import pytest
from rgbxyzlab import rgb_to_hls
from rgbxyzlab import primaries

# pytest.approx considers numbers within a relative tolerance of 1e-6

def test_rgb_to_hls_red () -> None:
    col = rgb_to_hls(primaries.rgb_red)
    assert col == pytest.approx(primaries.hls_red)

def test_rgb_to_hls_green () -> None:
    col = rgb_to_hls(primaries.rgb_green)
    assert col == pytest.approx(primaries.hls_green)

def test_rgb_to_hls_blue () -> None:
    col = rgb_to_hls(primaries.rgb_blue)
    assert col == pytest.approx(primaries.hls_blue)

def test_rgb_to_hls_yellow () -> None:
    col = rgb_to_hls(primaries.rgb_yellow)
    assert col == pytest.approx(primaries.hls_yellow)

def test_rgb_to_hls_magenta () -> None:
    col = rgb_to_hls(primaries.rgb_magenta)
    assert col == pytest.approx(primaries.hls_magenta)

def test_rgb_to_hls_cyan () -> None:
    col = rgb_to_hls(primaries.rgb_cyan)
    assert col == pytest.approx(primaries.hls_cyan)

def test_rgb_to_hls_white () -> None:
    col = rgb_to_hls(primaries.rgb_white)
    assert col == pytest.approx(primaries.hls_white, abs=1e-7)

def test_rgb_to_hls_black () -> None:
    col = rgb_to_hls(primaries.rgb_black)
    assert col == primaries.hls_black
