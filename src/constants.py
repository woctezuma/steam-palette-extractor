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
CIELAB_PALETTE_FNAME: str = f"{PALETTE_BASE_NAME}_lab.pth"
CIELUV_PALETTE_FNAME: str = f"{PALETTE_BASE_NAME}_luv.pth"

MAX_NUM_DISPLAYED_IMAGES: int = 25
DISPLAYED_IMAGE_WIDTH: int = 300

COLOR_SPACES = [
    "rgb",
    "hsv",
    "linear_hsv",
    "cielab",
    "cieluv",
]

PALETTE_DISTANCES = [
    "sum_pairwise_distances",
    "hausdorff_distance",
    "custom_hausdorff_distance",
]


def get_default_params() -> dict[str, float | int | str]:
    return {
        "exponent": 1.0,
        "factor": 1.0,
        "topk": 0,
        "max_num_popular_app_ids": 1e5,
        "color_space": "linear_hsv",
        "palette_distance": "custom_hausdorff_distance",
    }
