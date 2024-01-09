def trim_popular_appids(popular_appids, params):
    max_num_popular_app_ids = int(
        min(
            len(popular_appids),
            max(
                0,
                params["max_num_popular_app_ids"],
            ),
        ),
    )

    return popular_appids[:max_num_popular_app_ids]
