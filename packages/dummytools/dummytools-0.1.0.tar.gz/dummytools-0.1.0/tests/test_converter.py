import pytest
from dummytools.converter import decimal_to_binary, binary_to_decimal


# ---------- Tests for decimal_to_binary ----------

def test_decimal_to_binary_basic():
    assert decimal_to_binary(0) == "0"
    assert decimal_to_binary(1) == "1"
    assert decimal_to_binary(2) == "10"
    assert decimal_to_binary(10) == "1010"
    assert decimal_to_binary(255) == "11111111"

def test_decimal_to_binary_type_error():
    with pytest.raises(TypeError):
        decimal_to_binary("10")
    with pytest.raises(TypeError):
        decimal_to_binary(3.14)

def test_decimal_to_binary_value_error():
    with pytest.raises(ValueError):
        decimal_to_binary(-1)


# ---------- Tests for binary_to_decimal ----------

def test_binary_to_decimal_basic():
    assert binary_to_decimal("0") == 0
    assert binary_to_decimal("1") == 1
    assert binary_to_decimal("10") == 2
    assert binary_to_decimal("1010") == 10
    assert binary_to_decimal("11111111") == 255

def test_binary_to_decimal_type_error():
    with pytest.raises(TypeError):
        binary_to_decimal(1010)
    with pytest.raises(TypeError):
        binary_to_decimal(None)

def test_binary_to_decimal_value_error():
    with pytest.raises(ValueError):
        binary_to_decimal("102")
    with pytest.raises(ValueError):
        binary_to_decimal("abc")
    with pytest.raises(ValueError):
        binary_to_decimal("10 01")  # contains space
