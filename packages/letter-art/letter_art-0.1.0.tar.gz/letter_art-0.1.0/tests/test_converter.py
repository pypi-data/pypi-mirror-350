from letter_art.converter import convert_image_to_ascii
import os

def test_ascii_output_format():
    ascii_art = convert_image_to_ascii("tests/sample.jpg", width=50)
    assert isinstance(ascii_art, str)
    assert "\n" in ascii_art
    assert len(ascii_art.splitlines()) > 1
