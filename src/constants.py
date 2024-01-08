APPID_FNAME: str = "appids.json"
POPULAR_APPIDS_FNAME: str = "popular_appids.json"
FILTERED_APP_IDS_FNAME: str = "filtered_appids.json"
FILTERED_INDICES_FNAME: str = "filtered_indices.json"
SOLUTIONS_FNAME: str = "egs_solutions.json"

IMG_FOLDER: str = "steam_images"
IMG_NAME: str = "capsule_616x353.jpg"

NUM_COLORS: int = 8
PALETTE_BASE_NAME: str = f"steam_palette_{NUM_COLORS}"
PALETTE_FNAME: str = f"{PALETTE_BASE_NAME}.pth"
HSV_PALETTE_FNAME: str = f"{PALETTE_BASE_NAME}_hsv.pth"

MAX_NUM_DISPLAYED_IMAGES: int = 25
DISPLAYED_IMAGE_WIDTH: int = 300


def get_default_params() -> dict[str, float | int | bool]:
    return {
        "exponent": 1.0,
        "factor": 1.0,
        "topk": 0,
        "max_num_popular_app_ids": 1e5,
        "use_hsv": True,
        "change_coordinates": True,
    }
