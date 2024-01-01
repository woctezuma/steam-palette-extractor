from colorsys import rgb_to_hsv

import mediapy as media
import torch
from PIL import Image

# Reference:
# https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image/61730849#61730849


def get_dominant_colors(
    pil_img,
    palette_size: int = 16,
    num_colors: int = 10,
) -> list[list[int]]:
    # Resize image to speed up processing
    img = pil_img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)

    dominant_colors = []
    for i in range(num_colors):
        try:
            palette_index = color_counts[i][1]
            colors = palette[palette_index * 3 : palette_index * 3 + 3]
        except IndexError:
            colors = [0, 0, 0]

        dominant_colors.append(colors)

    return dominant_colors


def extract_colors(path_or_url: str, num_colors: int = 10) -> list[list[int]]:
    img = media.read_image(path_or_url)
    pil_img = Image.fromarray(img)
    return get_dominant_colors(pil_img, num_colors=num_colors)


def to_hsv(r: int, g: int, b: int) -> tuple(int):
    # Reference: https://stackoverflow.com/a/37656972/376454

    h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
    return int(h * 255), int(s * 255), int(v * 255)


def to_linear_hsv(
    dominant_colors: list[list[int]],
    change_coordinates: bool = True,
) -> torch.tensor:
    v = torch.tensor([to_hsv(*rgb) for rgb in dominant_colors])

    # Caveat: convert the HSV values before computing the distance!
    # https://stackoverflow.com/a/39113477/376454

    if change_coordinates:
        v = v.float() / 255

        theta = 2 * torch.pi * v[:, 0]
        radius = v[:, 1]

        x = radius * torch.cos(theta)
        y = radius * torch.sin(theta)

        v[:, 0] = x
        v[:, 1] = y

    return v
