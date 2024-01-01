def to_steam_url(app_id, egs_solutions) -> str:
    elements = egs_solutions["image"]["steam"]
    return f"{elements['url']}{app_id}{elements['suffix']}"


def to_egs_url(egs_solutions, index, md5) -> str:
    elements = egs_solutions["image"]["egs"]
    keyword = elements["keyword"][0] if index == 1 else elements["keyword"][1]
    return f"{elements['url']}{index}{keyword}{elements['resolution']}{md5}"


def from_gift_to_steam_url(egs_solutions, gift, app_id_index=0):
    app_id = gift["appids"][app_id_index]
    return to_steam_url(egs_solutions, app_id)


def from_gift_to_egs_url(egs_solutions, gift):
    index = gift["index"]
    md5 = gift["md5"]
    return to_egs_url(egs_solutions, index, md5)
