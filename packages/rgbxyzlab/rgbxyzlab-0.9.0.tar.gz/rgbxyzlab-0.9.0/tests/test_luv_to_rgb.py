import pytest
from rgbxyzlab import xyz_to_luv, luv_to_xyz
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_luv_to_xyz_red () -> None:

    col = xyz_to_luv(primaries.xyz_red)
    col = luv_to_xyz(col)
    assert col == pytest.approx(primaries.xyz_red)

def test_xyz_to_luv_green () -> None:
    col = xyz_to_luv(primaries.xyz_green)
    col = luv_to_xyz(col)
    assert col == pytest.approx(primaries.xyz_green)

def test_xyz_to_luv_blue () -> None:
    col = xyz_to_luv(primaries.xyz_blue)
    col = luv_to_xyz(col)
    assert col == pytest.approx(primaries.xyz_blue)

def test_xyz_to_luv_yellow () -> None:
    col = xyz_to_luv(primaries.xyz_yellow)
    col = luv_to_xyz(col)
    assert col == pytest.approx(primaries.xyz_yellow)

def test_xyz_to_luv_magenta () -> None:
    col = xyz_to_luv(primaries.xyz_magenta)
    col = luv_to_xyz(col)
    assert col == pytest.approx(primaries.xyz_magenta)

def test_xyz_to_luv_cyan () -> None:
    col = xyz_to_luv(primaries.xyz_cyan)
    col = luv_to_xyz(col)
    assert col == pytest.approx(primaries.xyz_cyan)

def test_xyz_to_luv_white () -> None:
    col = xyz_to_luv(primaries.xyz_white)
    col = luv_to_xyz(col)
    assert col == pytest.approx(primaries.xyz_white, abs=1e-7)

def test_xyz_to_luv_black () -> None:
    col = xyz_to_luv(primaries.xyz_black)
    col = luv_to_xyz(col)
    assert col == primaries.xyz_black
