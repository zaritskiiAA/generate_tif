def concat_query_params(params: dict[str, str]):
    """Преобразование query params."""

    result = [
        f'?{param[0]}={param[1]}' if not idx else f'&{param[0]}={param[1]}' for idx, param in enumerate(params.items()) # noqa E501
    ]

    return ''.join(result)
