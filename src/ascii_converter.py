from PIL import Image

DEFAULT_CHARSET = "@%#*+=-:. "

def resize_image(image, new_width):
    width, height = image.size

    # Characters are taller than they are wide
    aspect_ration = height / width
    new_height = int(new_width * aspect_ration * 0.55)

    return image.resize((new_width, new_height))

def pixel_to_char(pixel_value, charset):
    index = int(pixel_value / 255 * (len(charset) - 1))
    return charset[index]

def image_to_ascii(image_path, width=120, charset=DEFAULT_CHARSET):
    image = Image.open(image_path).convert("RGB")

    image = resize_image(image, width)

    ascii_lines = []

    for y in range(image.height):
        line = ""

        for x in range(image.width):
            r, g, b = image.getpixel((x, y))

            gray = int((r + g + b) / 3)

            line += pixel_to_char(gray, charset)

        ascii_lines.append(line)

    return "\n".join(ascii_lines)