import os
import io
import zipfile

import numpy as np
import tifffile
from PIL import Image

from .constants import FILE_NAME, MEDIA_PATH


def read_stream_and_save_content(content: bytes, media_path: str):
    """
    Преобразование байтов в поток байтов,
    чтение архива и сохраниение контента в media_path для дальнейшей работы.
    """

    stream = io.BytesIO(content)
    with zipfile.ZipFile(stream) as archive:
        archive.extractall(media_path)


class GenerateTiffFile:
    """ Класс для генерации tiff файла."""

    def __init__(
            self,
            several_images: list[str],
            response_href: str,
            media_path: str = MEDIA_PATH,
            output_file_name: str = FILE_NAME,
    ) -> None:

        self.several_images = several_images
        self.media_path = media_path
        self.response_href = response_href
        self.output_file_name = output_file_name

    @property
    def output_file_name(self) -> str:
        return self._output_file_name

    @output_file_name.setter
    def output_file_name(self, file_name: str) -> None:
        self._output_file_name = os.path.join(self.media_path, file_name)

    @property
    def response_href(self):
        return self._response_href

    @response_href.setter
    def response_href(self, value):
        self._response_href = os.path.join(value, f'media/{FILE_NAME}')

    def generate(self) -> str:

        self._create_result_dir()
        images_data = []
        row_data = []

        for idx, image in enumerate(self.several_images, start=1):
            with Image.open(image) as img_pil:
                weight, height = img_pil.size
                frame_img = Image.new(
                    "RGB", (weight + 20, height + 20), "white",
                )

                frame_img.paste(img_pil, (10, 10))
                img_array = np.array(frame_img.convert('RGB'))
                images_data.append(img_array)

                if idx % 4 == 0:
                    combined_image_data = np.concatenate(images_data, axis=1)
                    row_data.append(combined_image_data)
                    images_data.clear()
        final_image_data = np.concatenate(row_data, axis=0)

        with tifffile.TiffWriter(self.output_file_name) as tif:
            tif.save(final_image_data)
        return self.response_href

    def _create_result_dir(self) -> None:
        os.makedirs(f'{self.media_path}/result/', exist_ok=True)
