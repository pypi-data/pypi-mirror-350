import pytest
from rgbxyzlab import hls_to_rgb
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_hls_to_rgb_red () -> None:
    col = hls_to_rgb(primaries.hls_red)
    assert col == pytest.approx(primaries.rgb_red, abs=1e-6)

def test_hls_to_rgb_green () -> None:
    col = hls_to_rgb(primaries.hls_green)
    assert col == pytest.approx(primaries.rgb_green, abs=1e-6)

def test_hls_to_rgb_blue () -> None:
    col = hls_to_rgb(primaries.hls_blue)
    assert col == pytest.approx(primaries.rgb_blue, abs=1e-6)

def test_hls_to_rgb_yellow () -> None:
    col = hls_to_rgb(primaries.hls_yellow)
    assert col == pytest.approx(primaries.rgb_yellow, abs=1e-6)

def test_hls_to_rgb_magenta () -> None:
    col = hls_to_rgb(primaries.hls_magenta)
    assert col == pytest.approx(primaries.rgb_magenta, abs=1e-6)

def test_hls_to_rgb_cyan () -> None:
    col = hls_to_rgb(primaries.hls_cyan)
    assert col == pytest.approx(primaries.rgb_cyan, abs=1e-6)

def test_hls_to_rgb_white () -> None:
    col = hls_to_rgb(primaries.hls_white)
    assert col == pytest.approx(primaries.rgb_white, abs=1e-6)

def test_hls_to_rgb_black () -> None:
    col = hls_to_rgb(primaries.hls_black)
    assert col == primaries.rgb_black
