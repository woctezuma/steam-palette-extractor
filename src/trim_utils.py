def trim_popular_appids(popular_appids, params):
    params["max_num_popular_app_ids"] = min(
        len(popular_appids),
        max(
            0,
            params["max_num_popular_app_ids"],
        ),
    )

    max_num_popular_app_ids = params["max_num_popular_app_ids"]
    test_app_ids = popular_appids[:max_num_popular_app_ids]

    return test_app_ids, params
