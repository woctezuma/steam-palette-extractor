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
    "modified_hausdorff_distance",
    "custom_hausdorff_distance",
]


def get_default_params() -> dict[str, float | int | str | None]:
    return {
        "color_space": "linear_hsv",
        "factor_ramp": 1.0,
        "factor_source": 1.0,
        "factor_target": 1.0,
        "max_num_popular_app_ids": 1e5,
        "palette_distance": "custom_hausdorff_distance",
        "low_threshold_ramp": 0.0,
        "high_threshold_ramp": None,
        "apply_ramp_in_color_distance": True,
        "apply_ramp_in_palette_distance": True,
        "apply_target_in_color_distance": True,
        "apply_target_in_palette_distance": True,
        "topk": 0,
    }
