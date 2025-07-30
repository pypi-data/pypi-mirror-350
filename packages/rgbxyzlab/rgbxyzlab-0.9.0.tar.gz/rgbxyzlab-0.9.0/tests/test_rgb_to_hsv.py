import pytest
from rgbxyzlab import rgb_to_hsv
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_rgb_to_hsv_red () -> None:
    col = rgb_to_hsv(primaries.rgb_red)
    assert col == pytest.approx(primaries.hsv_red)

def test_rgb_to_hsv_green () -> None:
    col = rgb_to_hsv(primaries.rgb_green)
    assert col == pytest.approx(primaries.hsv_green)

def test_rgb_to_hsv_blue () -> None:
    col = rgb_to_hsv(primaries.rgb_blue)
    assert col == pytest.approx(primaries.hsv_blue)

def test_rgb_to_hsv_yellow () -> None:
    col = rgb_to_hsv(primaries.rgb_yellow)
    assert col == pytest.approx(primaries.hsv_yellow)

def test_rgb_to_hsv_magenta () -> None:
    col = rgb_to_hsv(primaries.rgb_magenta)
    assert col == pytest.approx(primaries.hsv_magenta)

def test_rgb_to_hsv_cyan () -> None:
    col = rgb_to_hsv(primaries.rgb_cyan)
    assert col == pytest.approx(primaries.hsv_cyan)

def test_rgb_to_hsv_white () -> None:
    col = rgb_to_hsv(primaries.rgb_white)
    assert col == pytest.approx(primaries.hsv_white, abs=1e-7)

def test_rgb_to_hsv_black () -> None:
    col = rgb_to_hsv(primaries.rgb_black)
    assert col == primaries.hsv_black
