from opengeh_bronze.infrastructure.contracts.decimal_value import DecimalValue


def test__from_decimal() -> None:
    # Arrange
    value = 12345.6789

    # Act
    result = DecimalValue.from_decimal(value)

    # Assert
    assert result.units == 12345
    assert result.nanos == 678900000


def test__to_decimal() -> None:
    # Arrange
    value = DecimalValue(12345, 678900000)

    # Act
    result = value.to_decimal()

    # Assert
    assert result == 12345.6789


def test__negative_value() -> None:
    # Arrange
    value = -12345.6789

    # Act
    result = DecimalValue.from_decimal(value)

    # Assert
    assert result.units == -12345
    assert result.nanos == -678900000
