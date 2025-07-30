import pytest
from rgbxyzlab import lab_to_rgb
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_lab_to_rgb_red () -> None:
    col = lab_to_rgb(primaries.lab_red)
    assert col == pytest.approx(primaries.rgb_red, abs=1e-6)

def test_lab_to_rgb_green () -> None:
    col = lab_to_rgb(primaries.lab_green)
    assert col == pytest.approx(primaries.rgb_green, abs=1e-6)

def test_lab_to_rgb_blue () -> None:
    col = lab_to_rgb(primaries.lab_blue)
    assert col == pytest.approx(primaries.rgb_blue, abs=1e-6)

def test_lab_to_rgb_yellow () -> None:
    col = lab_to_rgb(primaries.lab_yellow)
    assert col == pytest.approx(primaries.rgb_yellow, abs=1e-6)

def test_lab_to_rgb_magenta () -> None:
    col = lab_to_rgb(primaries.lab_magenta)
    assert col == pytest.approx(primaries.rgb_magenta, abs=1e-6)

def test_lab_to_rgb_cyan () -> None:
    col = lab_to_rgb(primaries.lab_cyan)
    assert col == pytest.approx(primaries.rgb_cyan, abs=1e-6)

def test_lab_to_rgb_white () -> None:
    col = lab_to_rgb(primaries.lab_white)
    assert col == pytest.approx(primaries.rgb_white, abs=1e-6)

def test_lab_to_rgb_black () -> None:
    col = lab_to_rgb(primaries.lab_black)
    assert col == primaries.rgb_black
