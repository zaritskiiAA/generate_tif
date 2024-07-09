from typing import Any

import requests

from .utils import concat_query_params


def send_request_to_ya_disk_api(
        url: str,
        method: str = 'GET',
        request_data: dict[str, Any] = {},
        query_params: dict[str, str] | None = None,
        **kwargs: dict[str, Any],
) -> requests.Response:
    """Функция для отправи http запроса с помощью библиотеки requests."""

    method = method.lower()

    if query_params:
        url = url + concat_query_params(query_params)
        print(url)
    if hasattr(requests, method):
        return getattr(requests, method)(url, **request_data, **kwargs)

    return requests.Response(
        {'method_not_allowed': 'Метод не обслуживается'},
        status=requests.status_codes.codes.NOT_ALLOWED,
    )
