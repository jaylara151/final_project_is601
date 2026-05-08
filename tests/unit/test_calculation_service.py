import pytest

from app.services.calculation_service import calculate_result


def test_addition():
    result = calculate_result(10, 5, "add")

    assert result == 15


def test_subtraction():
    result = calculate_result(10, 5, "subtract")

    assert result == 5


def test_multiplication():
    result = calculate_result(10, 5, "multiply")

    assert result == 50


def test_division():
    result = calculate_result(10, 5, "divide")

    assert result == 2


def test_division_by_zero():
    with pytest.raises(ValueError):
        calculate_result(10, 0, "divide")


def test_invalid_operation():
    with pytest.raises(ValueError):
        calculate_result(10, 5, "wrong")