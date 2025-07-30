import pytest
from rgbxyzlab import rgb_to_lab
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_rgb_to_lab_red () -> None:
    col = rgb_to_lab(primaries.rgb_red)
    assert col == pytest.approx(primaries.lab_red)

def test_rgb_to_lab_green () -> None:
    col = rgb_to_lab(primaries.rgb_green)
    assert col == pytest.approx(primaries.lab_green)

def test_rgb_to_lab_blue () -> None:
    col = rgb_to_lab(primaries.rgb_blue)
    assert col == pytest.approx(primaries.lab_blue)

def test_rgb_to_lab_yellow () -> None:
    col = rgb_to_lab(primaries.rgb_yellow)
    assert col == pytest.approx(primaries.lab_yellow)

def test_rgb_to_lab_magenta () -> None:
    col = rgb_to_lab(primaries.rgb_magenta)
    assert col == pytest.approx(primaries.lab_magenta)

def test_rgb_to_lab_cyan () -> None:
    col = rgb_to_lab(primaries.rgb_cyan)
    assert col == pytest.approx(primaries.lab_cyan)

def test_rgb_to_lab_white () -> None:
    col = rgb_to_lab(primaries.rgb_white)
    assert col == pytest.approx(primaries.lab_white, abs=1e-7)

def test_rgb_to_lab_black () -> None:
    col = rgb_to_lab(primaries.rgb_black)
    assert col == primaries.lab_black
