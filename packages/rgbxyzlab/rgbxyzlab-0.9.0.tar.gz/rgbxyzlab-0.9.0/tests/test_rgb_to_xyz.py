import pytest
from rgbxyzlab import rgb_to_xyz
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_rgb_to_xyz_red () -> None:
    col = rgb_to_xyz(primaries.rgb_red)
    assert col == pytest.approx(primaries.xyz_red)

def test_rgb_to_xyz_green () -> None:
    col = rgb_to_xyz(primaries.rgb_green)
    assert col == pytest.approx(primaries.xyz_green)

def test_rgb_to_xyz_blue () -> None:
    col = rgb_to_xyz(primaries.rgb_blue)
    assert col == pytest.approx(primaries.xyz_blue)

def test_rgb_to_xyz_yellow () -> None:
    col = rgb_to_xyz(primaries.rgb_yellow)
    assert col == pytest.approx(primaries.xyz_yellow)

def test_rgb_to_xyz_magenta () -> None:
    col = rgb_to_xyz(primaries.rgb_magenta)
    assert col == pytest.approx(primaries.xyz_magenta)

def test_rgb_to_xyz_cyan () -> None:
    col = rgb_to_xyz(primaries.rgb_cyan)
    assert col == pytest.approx(primaries.xyz_cyan)

def test_rgb_to_xyz_white () -> None:
    col = rgb_to_xyz(primaries.rgb_white)
    assert col == pytest.approx(primaries.xyz_white)

def test_rgb_to_xyz_black () -> None:
    col = rgb_to_xyz(primaries.rgb_black)
    assert col == primaries.xyz_black
