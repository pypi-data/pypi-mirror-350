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

Convert any image to ASCII text art

Customizable **width** and **height**

Choose to **print** the result or **save as .txt file**

Minimal dependencies (`Pillow` only)

---

## Quick Start

```python
from letter_art.converter import convert_image_to_ascii

# Basic usage: terminal output
convert_image_to_ascii("sample.jpg", width=100, height=50, output="print")

# Save to a file
convert_image_to_ascii("sample.jpg", width=120, height=60, output="file", output_path="ascii_output.txt")

```

---

## ⚙️ Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `image_path` | `str` | (required) | Path to input image |
| `width` | `int` | `100` | Width in **characters**, not pixels |
| `height` | `int` | calculated | Height in characters (optional) |
| `output` | `str` | `"print"` | `"print"` for terminal, `"file"` for saving to `.txt` |
| `output_path` | `str` | `"output.txt"` | Path to output `.txt` file if `output="file"` |

---

## Example CLI Interaction

```bash
$ python test_ascii.py
출력 방식을 선택하세요 (print / file): file
저장할 파일명을 입력하세요 (예: result.txt): ascii_art.txt
✔ ASCII 아트가 ascii_art.txt에 저장되었습니다.

```

---

## Recommended Images

High contrast images

Portrait-style or logos

Grayscale-friendly designs

---