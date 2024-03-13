# Copyright 2024 KubeAGI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
from pathlib import Path
from typing import List

from kubeagi_core.document_loaders.base import BaseLoader
from langchain_community.document_loaders import PyPDFLoader
from PIL import Image
from unstructured.partition.pdf import partition_pdf

logger = logging.getLogger(__name__)


class PDFLoader(BaseLoader):
    """Load pdf file."""

    def __init__(
        self,
        file_path: str,
    ):
        """
        Initialize the loader with a list of URL paths.

        Args:
            file_path (str): File Path.
        """
        self._file_path = file_path

    def load(self) -> List:
        """
        Load and return all Documents from the docx file.

        Returns:
            List[Document]: A list of Document objects.

        """
        logger.info("Start to load pdf file")

        # Get file name
        path = Path(self._file_path)
        file_name = path.name

        pdf_loader = PyPDFLoader(self._file_path)
        documents = pdf_loader.load()
        for document in documents:
            document.metadata["source"] = file_name

        return documents

    def extract_images(
        self,
        output_dir: str,
        remove_small_images: bool = False,
        min_width: int = 400,
        min_height: int = 100,
    ):
        """
        extract images.

        Args:
            output_dir (str)
                output image path.
            remove_small_images
                Is it necessary to filter out smaller images.
                the default value is set to False.
            min_width
                Only applicable if `remove_small_images=True`.
                The minimum width of the image.
            min_height
                Only applicable if `remove_small_images=True`.
                The minimum height of the image.
        """
        try:
            partition_pdf(
                filename=self._file_path,
                strategy="hi_res",
                extract_images_in_pdf=True,
                extract_image_block_output_dir=output_dir,
            )

            if remove_small_images:
                for filename in os.listdir(output_dir):
                    if filename.lower().endswith(
                        (".png", ".jpg", ".jpeg", ".gif", ".bmp")
                    ):
                        file_path = os.path.join(output_dir, filename)
                        with Image.open(file_path) as img:
                            width, height = img.size
                            if width < min_width and height < min_height:
                                os.remove(file_path)
        except Exception as e:
            logger.info(f"extract images fail: {e}")
