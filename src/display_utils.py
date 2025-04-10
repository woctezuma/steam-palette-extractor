import mediapy as media
import torch
from PIL import Image, ImageDraw

from src.constants import DISPLAYED_IMAGE_WIDTH, MAX_NUM_DISPLAYED_IMAGES, NUM_COLORS
from src.download_utils import get_image_url

# Reference: https://stackoverflow.com/questions/54165439/what-are-the-exact-color-names-available-in-pils-imagedraw


def show_colors(c: list[list[int]]) -> None:
    n = len(c)

    cols = NUM_COLORS
    rows = ((n - 1) // cols) + 1
    cell_height = 30
    cell_width = 170
    img_height = cell_height * rows
    img_width = cell_width * cols

    i = Image.new("RGB", (img_width, img_height), (0, 0, 0))
    a = ImageDraw.Draw(i)

    for idx, rgb in enumerate(c):
        y0 = cell_height * (idx // cols)
        y1 = y0 + cell_height
        x0 = cell_width * (idx % cols)
        x1 = x0 + (cell_width / 1)

        a.rectangle([x0, y0, x1, y1], fill=tuple(rgb), outline="black")

    media.show_image(i)


def display_results(
    most_similar_app_ids: list[str],
    indices: list[int],
    distances: torch.tensor,
    max_num_displayed_images: int = MAX_NUM_DISPLAYED_IMAGES,
    displayed_image_width: int = DISPLAYED_IMAGE_WIDTH,
) -> None:
    for i, app_id in enumerate(
        most_similar_app_ids[:max_num_displayed_images],
    ):
        distance = distances[indices[i]]

        path_or_url = get_image_url(app_id)
        print(
            f"\t{i + 1}) appID: {app_id} ; distance: {distance:.2f} ; url: {path_or_url}",
        )
        media.show_image(media.read_image(path_or_url), width=displayed_image_width)
