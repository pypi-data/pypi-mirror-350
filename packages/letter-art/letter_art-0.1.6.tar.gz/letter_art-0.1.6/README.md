# letter-art

Convert images into ASCII art with adjustable resolution and output format.

A simple and fun Python library to turn your images into terminal-ready retro text art.

---

## Installation

```bash
pip install letter-art

```

---

## Features

- Convert any image to ASCII text art
- Customizable **width**, **height**, and **character aspect ratio**
- Choose to **print** the result or **save it as a .txt / .html file**
- CLI (Command Line Interface) support
- Minimal dependencies (`Pillow` only)

---

## Quick Start (in Python)

```python
from letter_art.converter import convert_image_to_ascii

# Basic usage: print to terminal
convert_image_to_ascii("sample.jpg", width=100, height=50, output="print")

# Save to a file
convert_image_to_ascii(
    image_path="sample.jpg",
    width=120,
    height=60,
    output="file",
    output_path="ascii_output.txt",
    output_format="txt"  # or "html"
)

```

---

## Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `image_path` | `str` | (required) | Path to the input image |
| `width` | `int` | `100` | Width of the ASCII art (in characters) |
| `height` | `int` | calculated | Height (optional). Auto-calculated if not provided |
| `output` | `str` | `"print"` | `"print"` for terminal output, `"file"` to save |
| `output_path` | `str` | auto-named | Path to output file if `output="file"` |
| `output_format` | `str` | `"txt"` | `"txt"` or `"html"` output format |
| `height_scale` | `float` | `0.6` | Vertical scale adjustment for character aspect ratio |

---

## CLI Usage

After installation, you can run it directly from the terminal using:

```bash
letter-art --image sample.jpg --width 150 --output file --format html

```

### CLI Options

| Option | Description |
| --- | --- |
| `--image` | Input image path (required) |
| `--width` | Width in characters (default: 300) |
| `--height` | Optional height |
| `--output` | `"print"` or `"file"` |
| `--output_path` | File path to save output (optional) |
| `--format` | `"txt"` or `"html"` |
| `--scale` | Vertical scaling factor (default 0.6) |

---

## Example CLI Output

```bash
$ letter-art --image test.jpg --width 200 --output file --format txt
✔ ASCII art saved to test.txt

```

---

## Recommended Images

- High-contrast images
- Logos, icons, or face portraits
- Grayscale-friendly content

---

## License

MIT License

(c) 2025 gwondoo