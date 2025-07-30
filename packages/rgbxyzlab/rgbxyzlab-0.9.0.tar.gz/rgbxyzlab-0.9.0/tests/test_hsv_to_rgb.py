import pytest
from rgbxyzlab import hsv_to_rgb
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_hsv_to_rgb_red () -> None:
    col = hsv_to_rgb(primaries.hsv_red)
    assert col == pytest.approx(primaries.rgb_red, abs=1e-6)

def test_hsv_to_rgb_green () -> None:
    col = hsv_to_rgb(primaries.hsv_green)
    assert col == pytest.approx(primaries.rgb_green, abs=1e-6)

def test_hsv_to_rgb_blue () -> None:
    col = hsv_to_rgb(primaries.hsv_blue)
    assert col == pytest.approx(primaries.rgb_blue, abs=1e-6)

def test_hsv_to_rgb_yellow () -> None:
    col = hsv_to_rgb(primaries.hsv_yellow)
    assert col == pytest.approx(primaries.rgb_yellow, abs=1e-6)

def test_hsv_to_rgb_magenta () -> None:
    col = hsv_to_rgb(primaries.hsv_magenta)
    assert col == pytest.approx(primaries.rgb_magenta, abs=1e-6)

def test_hsv_to_rgb_cyan () -> None:
    col = hsv_to_rgb(primaries.hsv_cyan)
    assert col == pytest.approx(primaries.rgb_cyan, abs=1e-6)

def test_hsv_to_rgb_white () -> None:
    col = hsv_to_rgb(primaries.hsv_white)
    assert col == pytest.approx(primaries.rgb_white, abs=1e-6)

def test_hsv_to_rgb_black () -> None:
    col = hsv_to_rgb(primaries.hsv_black)
    assert col == primaries.rgb_black
