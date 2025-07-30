import pytest
from rgbxyzlab import hex_to_lab
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_hex_to_lab_red () -> None:
    col = hex_to_lab("#f00")
    assert col == pytest.approx(primaries.lab_red)

def test_hex_to_lab_green () -> None:
    col = hex_to_lab("#0f0")
    assert col == pytest.approx(primaries.lab_green)

def test_hex_to_lab_blue () -> None:
    col = hex_to_lab("#00f")
    assert col == pytest.approx(primaries.lab_blue)

def test_hex_to_lab_yellow () -> None:
    col = hex_to_lab("#ff0")
    assert col == pytest.approx(primaries.lab_yellow)

def test_hex_to_lab_magenta () -> None:
    col = hex_to_lab("#f0f")
    assert col == pytest.approx(primaries.lab_magenta)

def test_hex_to_lab_cyan () -> None:
    col = hex_to_lab("#0ff")
    assert col == pytest.approx(primaries.lab_cyan)

def test_hex_to_lab_white () -> None:
    col = hex_to_lab("#fff")
    assert col == pytest.approx(primaries.lab_white, abs=1e-7)

def test_hex_to_lab_black () -> None:
    col = hex_to_lab("#000")
    assert col == primaries.lab_black
