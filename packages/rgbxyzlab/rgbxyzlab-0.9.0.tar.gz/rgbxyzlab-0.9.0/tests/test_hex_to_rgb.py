from rgbxyzlab import hex_to_rgb
from rgbxyzlab import primaries

def test_hex_to_rgb_red () -> None:
    col = hex_to_rgb("#f00")
    assert col == primaries.rgb_red

def test_hex_to_rgb_green () -> None:
    col = hex_to_rgb("#0f0")
    assert col == primaries.rgb_green

def test_hex_to_rgb_blue () -> None:
    col = hex_to_rgb("#00f")
    assert col == primaries.rgb_blue

def test_hex_to_rgb_yellow () -> None:
    col = hex_to_rgb("#ff0")
    assert col == primaries.rgb_yellow

def test_hex_to_rgb_magenta () -> None:
    col = hex_to_rgb("#f0f")
    assert col == primaries.rgb_magenta

def test_hex_to_rgb_cyan () -> None:
    col = hex_to_rgb("#0ff")
    assert col == primaries.rgb_cyan

def test_hex_to_rgb_white () -> None:
    col = hex_to_rgb("#fff")
    assert col == primaries.rgb_white

def test_hex_to_rgb_black () -> None:
    col = hex_to_rgb("#000")
    assert col == primaries.rgb_black
