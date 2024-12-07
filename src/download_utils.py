from pathlib import Path

from src.constants import IMG_NAME


def get_image_url(app_id: str, img_name: str = IMG_NAME) -> str:
    return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/{img_name}"


def write_to_text_file(
    app_ids: list[str],
    fname: str,
    img_name: str = IMG_NAME,
) -> None:
    with Path(fname).open("w", encoding="utf-8") as f:
        for app_id in app_ids:
            url = get_image_url(app_id, img_name)
            f.write(f"{url}\n")
