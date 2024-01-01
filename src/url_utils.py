def to_steam_url(app_id, egs_solutions) -> str:
    elements = egs_solutions["image"]["steam"]
    return f"{elements['url']}{app_id}{elements['suffix']}"


def to_egs_url(egs_solutions: dict, index: int, md5: str) -> str:
    elements = egs_solutions["image"]["egs"]
    keyword = elements["keyword"][0] if index == 1 else elements["keyword"][1]
    return f"{elements['url']}{index}{keyword}{elements['resolution']}{md5}"


def from_gift_to_steam_url(
    egs_solutions: dict,
    gift: dict,
    app_id_index: int = 0,
) -> str:
    app_id = gift["appids"][app_id_index]
    return to_steam_url(egs_solutions, app_id)


def from_gift_to_egs_url(egs_solutions: dict, gift: dict) -> str:
    index = gift["index"]
    md5 = gift["md5"]
    return to_egs_url(egs_solutions, index, md5)
