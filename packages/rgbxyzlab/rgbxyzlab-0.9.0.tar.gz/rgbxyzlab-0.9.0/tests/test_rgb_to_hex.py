from rgbxyzlab import rgb_to_hex
from rgbxyzlab import primaries


def test_rgb_to_hex_red () -> None:
    col = rgb_to_hex(primaries.rgb_red)
    assert col == "#ff0000"

def test_rgb_to_hex_green () -> None:
    col = rgb_to_hex(primaries.rgb_green)
    assert col == "#00ff00"

def test_rgb_to_hex_blue () -> None:
    col = rgb_to_hex(primaries.rgb_blue)
    assert col == "#0000ff"

def test_rgb_to_hex_yellow () -> None:
    col = rgb_to_hex(primaries.rgb_yellow)
    assert col == "#ffff00"

def test_rgb_to_hex_magenta () -> None:
    col = rgb_to_hex(primaries.rgb_magenta)
    assert col == "#ff00ff"

def test_rgb_to_hex_cyan () -> None:
    col = rgb_to_hex(primaries.rgb_cyan)
    assert col == "#00ffff"

def test_rgb_to_hex_white () -> None:
    col = rgb_to_hex(primaries.rgb_white)
    assert col == "#ffffff"

def test_rgb_to_hex_black () -> None:
    col = rgb_to_hex(primaries.rgb_black)
    assert col == "#000000"
