import json
import os
import logging
import glob

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from service.ya_disk_api import send_request_to_ya_disk_api
from .constants import (
    PUB_RESOURCES_ENDPOINT,
    YA_DISK_API_URL,
    PUB_FOLDER,
    MEDIA_PATH,
)
from .utils import read_stream_and_save_content, GenerateTiffFile


logger = logging.getLogger(__name__)


class CreateTiffFile(CreateAPIView):
    """
    Представление для генерации tiff файла из исходных файлов на Я.диске.
    Возвращает ссылку для автозагрузки готового tiff файла.
    """

    def create(self, request, *args, **kwargs):

        logger.info('Запрос к эндпоинту по созданию tiff файла')

        url = os.path.join(YA_DISK_API_URL, PUB_RESOURCES_ENDPOINT)
        query_params = {'public_key': PUB_FOLDER}

        response_public_resources = send_request_to_ya_disk_api(
            url, query_params=query_params,
        )

        if response_public_resources.status_code != 200:
            logger.error(
                (
                    f'При запросе произошла к {url} '
                    f'ошибка {response_public_resources.status_code}'
                )
            )
            return Response(
                {'error': 'Что-то пошло не так'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # TODO: здесь можно использовать сериализатор
        # для гарантии валидного ответа.
        parse_data = json.loads(response_public_resources.content)
        download_reponse = send_request_to_ya_disk_api(
            parse_data['href'], parse_data['method'],
        )

        if download_reponse.status_code != 200:
            logger.error(
                (
                    f'При запросе к {parse_data["href"]} '
                    f'произошла ошибка {download_reponse.status_code}'
                )
            )
            return Response(
                {'error': 'Что-то пошло не так'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # TODO: аналогично комментарию выше.
        read_stream_and_save_content(download_reponse.content, MEDIA_PATH)

        png_files = [
            obj for obj in glob.glob(f'{MEDIA_PATH}/**/*.png', recursive=True) if os.path.isfile(obj) # noqa E501
        ]
        tiff = GenerateTiffFile(png_files, f'http://{self.request.get_host()}')
        href = tiff.generate()

        return Response({'response': f'{href}'}, status=status.HTTP_200_OK)
