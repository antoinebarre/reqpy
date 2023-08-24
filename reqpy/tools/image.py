import random
from PIL import Image


def generate_random_image(
        width: int,
        height: int
        ) -> Image.Image:
    img = Image.new("RGB", (width, height))
    pixels = []
    for _ in range(width * height):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        pixels.append((r, g, b))

    img.putdata(pixels)
    return img
    