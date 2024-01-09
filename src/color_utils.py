from colorsys import rgb_to_hsv

import mediapy as media
import skimage as ski
import torch
from PIL import Image
from tqdm import tqdm

# Reference:
# https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image/61730849#61730849


def get_dominant_colors(
    pil_img: Image,
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


def to_hsv(r: int, g: int, b: int) -> tuple[int, int, int]:
    # Reference: https://stackoverflow.com/a/37656972/376454

    h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
    return int(h * 255), int(s * 255), int(v * 255)


def to_color_space(rgb, output_color_space="rgb"):
    if output_color_space.endswith("lab"):
        return ski.color.rgb2lab(rgb / 255)
    if output_color_space.endswith("luv"):
        return ski.color.rgb2luv(rgb / 255)
    if output_color_space in ["hsv", "hsl"]:
        return to_hsv(*rgb)
    return list(rgb)


def to_color_space_sequential(
    palettes: torch.tensor,
    output_color_space: str = "hsv",
) -> torch.tensor:
    palette_iterator = tqdm(palettes) if len(palettes) > 1 else palettes

    v_aggregated = None
    for dominant_colors in palette_iterator:
        v = torch.tensor(
            [
                to_color_space(rgb, output_color_space=output_color_space)
                for rgb in dominant_colors
            ],
        ).unsqueeze(dim=0)

        if v_aggregated is None:
            v_aggregated = v
        else:
            v_aggregated = torch.cat((v_aggregated, v), dim=0)

    return v_aggregated


def to_hsv_sequential(
    palettes: torch.tensor,
) -> torch.tensor:
    return to_color_space_sequential(palettes, output_color_space="hsv")


def change_hsv_coordinates_vectorized(
    palettes: torch.tensor,
) -> torch.tensor:
    # Convert the HSV values before computing the distance!
    # https://stackoverflow.com/a/39113477/376454

    v = palettes.float() / 255

    hue = v[:, :, 0]
    saturation = v[:, :, 1]

    theta = 2 * torch.pi * hue
    radius = saturation

    x = radius * torch.cos(theta)
    y = radius * torch.sin(theta)

    v[:, :, 0] = x
    v[:, :, 1] = y

    return v


def to_linear_hsv(
    dominant_colors: list[list[int]],
    change_coordinates: bool = True,
) -> torch.tensor:
    v = to_hsv_sequential(dominant_colors)

    if change_coordinates:
        v = change_hsv_coordinates_vectorized(v)

    return v
