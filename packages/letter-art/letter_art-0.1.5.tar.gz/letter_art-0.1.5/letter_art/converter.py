from PIL import Image
from typing import Optional

ASCII_CHARS = "@%#*+=-:. "

def convert_image_to_ascii(
    image_path: str,
    width: int = 100,
    height: Optional[int] = None,
    output: str = "print",         # "print" or "file"
    output_path: str = "output.txt"
) -> Optional[str]:
    image = Image.open(image_path).convert("L")

    # 자동 높이 계산 또는 사용자 지정
    if height is None:
        aspect_ratio = image.height / image.width
        height = int(aspect_ratio * width * 0.5)

    image = image.resize((width, height))
    pixels = image.getdata()

    ascii_str = "".join(
        ASCII_CHARS[min(pixel * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)]
        for pixel in pixels
    )
    ascii_img = "\n".join(
        ascii_str[i:i+width] for i in range(0, len(ascii_str), width)
    )

    if output == "print":
        print(ascii_img)
        return ascii_img
    elif output == "file":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ascii_img)
        print(f"[✔] ASCII 아트가 {output_path}에 저장되었습니다.")
        return None
    else:
        raise ValueError("output 값은 'print' 또는 'file'이어야 합니다.")
