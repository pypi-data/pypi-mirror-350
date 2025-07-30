from PIL import Image
from typing import Optional
import os
import argparse

ASCII_CHARS = "@%#*+=-:. "

def convert_image_to_ascii(
    image_path: str,
    width: int = 300,
    height: Optional[int] = None,
    output: str = "print",
    output_path: Optional[str] = None,
    output_format: str = "txt",
    height_scale: float = 0.6
) -> Optional[str]:
    image = Image.open(image_path).convert("L")

    if height is None:
        aspect_ratio = image.height / image.width
        height = int(aspect_ratio * width * height_scale)

    image = image.resize((width, height))
    pixels = image.getdata()

    ascii_str = "".join(
        ASCII_CHARS[min(pixel * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)]
        for pixel in pixels
    )

    ascii_img = "\n".join(
        ascii_str[i:i + width] for i in range(0, len(ascii_str), width)
    )

    if output == "print":
        if output_format == "html":
            ascii_img = f"<pre style='font-family: monospace;'>{ascii_img}</pre>"
        print(ascii_img)
        return ascii_img

    elif output == "file":
        if output_path is None:
            base = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"{base}.{output_format}"
        if output_format == "html":
            html = f"<pre style='font-family: monospace;'>{ascii_img}</pre>"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(ascii_img)

        print(f"[✔] ASCII 아트가 '{output_path}'에 저장되었습니다.")
        return None

    else:
        raise ValueError("output 값은 'print' 또는 'file'이어야 합니다.")

def main():
    parser = argparse.ArgumentParser(description="Convert an image into ASCII art.")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image file")
    parser.add_argument("--width", type=int, default=300, help="Width of the ASCII art output")
    parser.add_argument("--height", type=int, help="Height of the ASCII art output (auto-calculated if omitted)")
    parser.add_argument("--output", type=str, choices=["print", "file"], default="print", help="Output mode: print to terminal or save to file")
    parser.add_argument("--output_path", type=str, help="Path to save the output file (used when output is 'file')")
    parser.add_argument("--format", type=str, choices=["txt", "html"], default="txt", help="Output file format: txt or html")
    parser.add_argument("--scale", type=float, default=0.6, help="Height scale factor to adjust character aspect ratio")

    args = parser.parse_args()

    convert_image_to_ascii(
        image_path=args.image,
        width=args.width,
        height=args.height,
        output=args.output,
        output_path=args.output_path,
        output_format=args.format,
        height_scale=args.scale
    )

if __name__ == "__main__":
    main()
