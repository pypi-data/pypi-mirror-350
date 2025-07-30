import pytest

from validio_sdk.resource import FieldDataType, FieldSelector
from validio_sdk.scalars import JsonTypeDefinition


@pytest.mark.parametrize(
    ("field_selector", "expected"),
    [
        (FieldSelector(data_type=FieldDataType.BOOLEAN), ["k1", "k2", "k9"]),
        (
            FieldSelector(
                data_type=FieldDataType.BOOLEAN,
                nullable=True,
            ),
            ["k1"],
        ),
        (FieldSelector(data_type=FieldDataType.BOOLEAN, regex="k(1|9)"), ["k1", "k9"]),
        (FieldSelector(data_type=FieldDataType.NUMERIC), ["k3", "k4", "k5", "k6"]),
        (FieldSelector(data_type=FieldDataType.STRING), ["k7"]),
        (FieldSelector(data_type=FieldDataType.TIMESTAMP), ["k8"]),
    ],
)
def test__get_matching_fields(
    field_selector: FieldSelector, expected: JsonTypeDefinition
) -> None:
    jtd_schema = {
        "optionalProperties": {
            "k1": {
                "type": "boolean",
                "nullable": True,
            },
            "k2": {
                "type": "boolean",
                "nullable": False,
            },
            "k3": {
                "type": "int16",
                "nullable": False,
            },
            "k4": {
                "type": "uint8",
                "nullable": False,
            },
            "k5": {
                "type": "float32",
                "nullable": False,
            },
            "k6": {
                "type": "float32",
                "nullable": False,
            },
            "k7": {
                "type": "string",
                "nullable": False,
            },
            "k8": {
                "type": "timestamp",
                "nullable": False,
            },
        },
        "properties": {
            "k9": {
                "type": "boolean",
                "nullable": False,
            },
        },
    }

    actual = field_selector._get_matching_fields(jtd_schema)
    assert set(expected) == set(actual)
