import pytest
from rgbxyzlab import lab_to_xyz
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_lab_to_xyz_red () -> None:
    col = lab_to_xyz(primaries.lab_red)
    assert col == pytest.approx(primaries.xyz_red)

def test_lab_to_xyz_green () -> None:
    col = lab_to_xyz(primaries.lab_green)
    assert col == pytest.approx(primaries.xyz_green)

def test_lab_to_xyz_blue () -> None:
    col = lab_to_xyz(primaries.lab_blue)
    assert col == pytest.approx(primaries.xyz_blue)

def test_lab_to_xyz_yellow () -> None:
    col = lab_to_xyz(primaries.lab_yellow)
    assert col == pytest.approx(primaries.xyz_yellow)

def test_lab_to_xyz_magenta () -> None:
    col = lab_to_xyz(primaries.lab_magenta)
    assert col == pytest.approx(primaries.xyz_magenta)

def test_lab_to_xyz_cyan () -> None:
    col = lab_to_xyz(primaries.lab_cyan)
    assert col == pytest.approx(primaries.xyz_cyan)

def test_lab_to_xyz_white () -> None:
    col = lab_to_xyz(primaries.lab_white)
    assert col == pytest.approx(primaries.xyz_white, abs=1e-6)

def test_lab_to_xyz_black () -> None:
    col = lab_to_xyz(primaries.lab_black)
    assert col == primaries.xyz_black
