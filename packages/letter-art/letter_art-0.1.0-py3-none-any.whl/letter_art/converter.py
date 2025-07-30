from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def convert_image_to_ascii(image_path: str, width: int = 100) -> str:
    image = Image.open(image_path).convert("L")
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width * 0.5)
    image = image.resize((width, new_height))
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel // 25] for pixel in pixels)
    ascii_img = "\n".join(ascii_str[i:i+width] for i in range(0, len(ascii_str), width))
    return ascii_img
