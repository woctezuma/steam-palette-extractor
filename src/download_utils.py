from pathlib import Path

from src.constants import IMG_NAME


def get_image_url(app_id, img_name=IMG_NAME) -> str:
    return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/{img_name}"


def write_to_text_file(app_ids, fname, img_name=IMG_NAME):
    with Path(fname).open("w") as f:
        for app_id in app_ids:
            url = get_image_url(app_id, img_name)
            f.write(f"{url}\n")
