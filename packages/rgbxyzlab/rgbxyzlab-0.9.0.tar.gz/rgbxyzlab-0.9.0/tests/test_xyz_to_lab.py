import pytest
from rgbxyzlab import xyz_to_lab
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_xyz_to_lab_red () -> None:
    col = xyz_to_lab(primaries.xyz_red)
    assert col == pytest.approx(primaries.lab_red)

def test_xyz_to_lab_green () -> None:
    col = xyz_to_lab(primaries.xyz_green)
    assert col == pytest.approx(primaries.lab_green)

def test_xyz_to_lab_blue () -> None:
    col = xyz_to_lab(primaries.xyz_blue)
    assert col == pytest.approx(primaries.lab_blue)

def test_xyz_to_lab_yellow () -> None:
    col = xyz_to_lab(primaries.xyz_yellow)
    assert col == pytest.approx(primaries.lab_yellow)

def test_xyz_to_lab_magenta () -> None:
    col = xyz_to_lab(primaries.xyz_magenta)
    assert col == pytest.approx(primaries.lab_magenta)

def test_xyz_to_lab_cyan () -> None:
    col = xyz_to_lab(primaries.xyz_cyan)
    assert col == pytest.approx(primaries.lab_cyan)

def test_xyz_to_lab_white () -> None:
    col = xyz_to_lab(primaries.xyz_white)
    assert col == pytest.approx(primaries.lab_white, abs=1e-7)

def test_xyz_to_lab_black () -> None:
    col = xyz_to_lab(primaries.xyz_black)
    assert col == primaries.lab_black
