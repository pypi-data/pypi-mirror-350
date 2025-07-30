import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from validio_sdk.scalars import JsonTypeDefinition


FIELD_SELECTOR_KEY = "_field_selector"


class FieldDataType(str, Enum):
    """Represents the datatype of a field."""

    STRING = "STRING"
    """
    Represents a string datatype.
    """
    NUMERIC = "NUMERIC"
    """
    Represents a numeric datatype: This is used for all integer and float types.
    """
    BOOLEAN = "BOOLEAN"
    """
    Represents a boolean datatype.
    """
    TIMESTAMP = "TIMESTAMP"
    """
    Represents a timestamp datatype.
    """

    def _matches(self, typename: str) -> bool:
        match self:
            case self.STRING:
                return typename == "string"
            case self.NUMERIC:
                return typename in {
                    "int8",
                    "uint8",
                    "int16",
                    "uint16",
                    "int32",
                    "uint32",
                    "float32",
                    "float64",
                }
            case self.BOOLEAN:
                return typename == "boolean"
            case self.TIMESTAMP:
                return typename == "timestamp"
            case _:
                return False


class FromFieldSelector:
    """
    A marker that can be provided as a reference field when declaring a Validator
    resource. It says to use the same source field as the reference field on the
    validator.
    """

    def _encode(self) -> dict[str, object]:
        return self.__dict__


@dataclass
class FieldSelector:
    """
    FieldSelector lets you select multiple fields at once to apply
    a validator on. It describes the attributes of the fields to be selected.
    """

    data_type: FieldDataType
    """
    Matches all fields that has the specified datatype.
    """
    nullable: bool | None = None
    """
    If provided, nullable narrows down the selected set of fields so far to only
    those that match the provided nullability. i.e if nullable is True,
    then only nullable fields will be selected.
    """
    regex: str | None = None
    """
    If provided, regex contains a regular expression pattern that will be matched
    against the selected set of fields so far and narrowed down to only those for
    which the regex match returns true on the field name.
    """

    @staticmethod
    def reference() -> FromFieldSelector:
        return FromFieldSelector()

    def _encode(self) -> dict[str, object]:
        return self.__dict__

    def _get_matching_fields(self, schema: "JsonTypeDefinition") -> list[str]:
        matching_fields = []
        properties: dict[str, dict[str, Any]] = {}
        for k in ["optionalProperties", "properties"]:
            if k in schema:
                properties = {**properties, **schema[k]}

        for name, prop in properties.items():
            if "type" not in prop or not FieldDataType[self.data_type]._matches(
                prop["type"]
            ):
                continue

            nullable_prop = True
            if "nullable" in prop:
                nullable_prop = prop["nullable"]
            if self.nullable and self.nullable != nullable_prop:
                continue

            if self.regex and not re.match(self.regex, name):
                continue

            matching_fields.append(name)

        return matching_fields

    @staticmethod
    def _replace(obj: dict[str, Any]) -> None:
        if FIELD_SELECTOR_KEY in obj:
            selector_obj = obj[FIELD_SELECTOR_KEY]
            obj[selector_obj["field_name"]] = FieldSelector(
                **selector_obj["field_selector"]
            )
            del obj[FIELD_SELECTOR_KEY]


@dataclass
class SelectorWithFieldName:
    """
    Internal: Helper class containing a field selector and the
    corresponding field name.
    """

    field_name: str
    field_selector: FieldSelector

    def _encode(self) -> dict[str, object]:
        return self.__dict__
