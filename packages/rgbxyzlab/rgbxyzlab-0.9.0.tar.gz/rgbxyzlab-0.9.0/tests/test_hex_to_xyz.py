import pytest
from rgbxyzlab import hex_to_xyz
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_hex_to_xyz_red () -> None:
    col = hex_to_xyz("#f00")
    assert col == pytest.approx(primaries.xyz_red)

def test_hex_to_xyz_green () -> None:
    col = hex_to_xyz("#0f0")
    assert col == pytest.approx(primaries.xyz_green)

def test_hex_to_xyz_blue () -> None:
    col = hex_to_xyz("#00f")
    assert col == pytest.approx(primaries.xyz_blue)

def test_hex_to_xyz_yellow () -> None:
    col = hex_to_xyz("#ff0")
    assert col == pytest.approx(primaries.xyz_yellow)

def test_hex_to_xyz_magenta () -> None:
    col = hex_to_xyz("#f0f")
    assert col == pytest.approx(primaries.xyz_magenta)

def test_hex_to_xyz_cyan () -> None:
    col = hex_to_xyz("#0ff")
    assert col == pytest.approx(primaries.xyz_cyan)

def test_hex_to_xyz_white () -> None:
    col = hex_to_xyz("#fff")
    assert col == pytest.approx(primaries.xyz_white)

def test_hex_to_xyz_black () -> None:
    col = hex_to_xyz("#000")
    assert col == primaries.xyz_black
