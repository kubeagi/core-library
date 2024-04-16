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
import fitz
import difflib
from pathlib import Path
from typing import List
from collections import Counter, defaultdict

from kubeagi_core.document import Document
from kubeagi_core.document_loaders.base import BaseLoader
from langchain_community.document_loaders import PyPDFLoader
from PIL import Image

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


class PyMuPDFLoader(BaseLoader):
    """Load pdf file using `PyMuPDF`."""

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

    def load(self) -> List[Document]:
        """
        Load and return all Documents from the pdf file.

        Returns:
            List[Document]: A list of Document objects.

        """
        logger.info("Start to load pdf file")

        # Get file name
        path = Path(self._file_path)
        file_name = path.name

        doc = fitz.open(self._file_path)

        pages = []
        for page in doc:
            text = page.get_text(sort=True)
            pages.append(text)
        doc.close()

        documents = []
        result = self._remove_run(pages)
        for i, item in enumerate(result):
            metadata = {"source": file_name, "page": i}
            documents.append(Document(page_content=item, metadata=metadata))

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
            doc = fitz.open(self._file_path)
            for i, item in enumerate(doc):
                image_list = item.get_images()

                # print the number of images found on the page
                for image_index, img in enumerate(
                    image_list, start=1
                ):  # enumerate the image list
                    xref = img[0]  # get the XREF of the image
                    pix = fitz.Pixmap(doc, xref)  # create a Pixmap

                    if pix.n - pix.alpha > 3:  # CMYK: convert to RGB first
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    output_file_name = (
                        output_dir
                        + "/figure-"
                        + str(i)
                        + "-"
                        + str(image_index)
                        + ".png"
                    )
                    pix.save(output_file_name)  # save the image as png
                    pix = None

            doc.close()

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

    def _remove_run(self, pages):
        page_to_remove = defaultdict(list)
        self._process_header(pages, page_to_remove)
        self._process_footer(pages, page_to_remove)

        result = []
        for i, item in enumerate(pages):  # 遍历每一页
            text = ""
            str = item.split("\n")  # 每一页按行分割
            delete_idx_in_page_i = page_to_remove[i]
            for idx, s in enumerate(str):
                if (
                    idx in delete_idx_in_page_i
                    or idx - len(str) in delete_idx_in_page_i
                ):
                    continue
                else:
                    text += s + "\n"
            text = text[:-1]

            result.append(text)
        return result

    def _process_header(self, pages, page_to_remove):
        avg_similar_score = 1
        vote_ratio = 1
        idx = 0
        skip_count = 0

        while avg_similar_score > 0.5 or vote_ratio > 0.5 or skip_count < 3:
            header_list = []
            header_content_len = []
            for item in pages:
                str = item.split("\n")
                header_list.append({"str": str[idx], "len": len(str[idx])})
                header_content_len.append(len(str[idx]))

            times = 0
            total_score = 0
            for i in range(0, len(header_list)):
                for j in range(i + 1, len(header_list)):
                    times += 1
                    score = self._string_similar(
                        header_list[i]["str"], header_list[j]["str"]
                    )
                    total_score += score
            avg_similar_score = total_score / times
            # 计算字符串相同长度出现最多次数的频率占比
            dic = Counter(header_content_len)
            dic = sorted(dic.items(), key=lambda item: item[1], reverse=True)
            vote_ratio = dic[0][1] / len(header_content_len)
            if avg_similar_score <= 0.5 and vote_ratio <= 0.5:
                if skip_count < 3:
                    skip_count += 1
                else:
                    break

            # 如果平均相似度>0.8，直接全部删除
            if avg_similar_score >= 0.8:
                for i, item in enumerate(pages):  # 遍历每一页
                    str = item.split("\n")  # 每一页按行分割
                    page_to_remove[i].append(idx)  # 第i页添加需要去掉的list索引
            # 如果相似度太低，按照最多相同长度为中心的[-2,2]范围，符合这个范围的页眉页脚都删掉
            else:
                for i, item in enumerate(header_list):  # 遍历每一页
                    if item["len"] >= dic[0][0] - 2 and item["len"] <= dic[0][0] + 2:
                        page_to_remove[i].append(idx)
            idx += 1

    def _process_footer(self, pages, page_to_remove):
        avg_similar_score = 1
        vote_ratio = 1
        idx = -1
        skip_count = 0

        while avg_similar_score > 0.5 or vote_ratio > 0.5 or skip_count < 3:
            header_list = []
            header_content_len = []
            for item in pages:
                str = item.split("\n")
                header_list.append({"str": str[idx], "len": len(str[idx])})
                header_content_len.append(len(str[idx]))

            times = 0
            total_score = 0
            for i in range(0, len(header_list)):
                for j in range(i + 1, len(header_list)):
                    times += 1
                    score = self._string_similar(
                        header_list[i]["str"], header_list[j]["str"]
                    )
                    total_score += score
            avg_similar_score = total_score / times
            # 计算字符串相同长度出现最多次数的频率占比
            dic = Counter(header_content_len)
            dic = sorted(dic.items(), key=lambda item: item[1], reverse=True)
            vote_ratio = dic[0][1] / len(header_content_len)
            if avg_similar_score <= 0.5 and vote_ratio <= 0.5:
                if skip_count < 3:
                    skip_count += 1
                else:
                    break

            # 如果平均相似度>0.8，直接全部删除
            if avg_similar_score >= 0.8:
                for i, item in enumerate(pages):  # 遍历每一页
                    page_to_remove[i].append(idx)  # 第i页添加需要去掉的list索引
            # 如果相似度太低，按照最多相同长度为中心的[-2,2]范围，符合这个范围的页眉页脚都删掉
            else:
                for i, item in enumerate(header_list):  # 遍历每一页
                    if item["len"] >= dic[0][0] - 2 and item["len"] <= dic[0][0] + 2:
                        page_to_remove[i].append(idx)
            idx -= 1

    def _string_similar(self, s1, s2):
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

    def extract_table(self):
        """
        extract table.
        """
        doc = fitz.open(self._file_path)

        tables = []
        for page_num, page in enumerate(doc):
            tabs = page.find_tables()
            for i, tab in enumerate(tabs.tables):
                headers = tab.header.names
                lines = tab.extract()

                tables.append(lines)
        doc.close()

        return tables

    def extract_table_to_markdown(self):
        """
        extract table to markdown.
        """
        doc = fitz.open(self._file_path)

        tables = []
        for page_num, page in enumerate(doc):
            tabs = page.find_tables()
            for i, tab in enumerate(tabs.tables):
                headers = tab.header.names
                lines = tab.extract()

                text = self._output_to_markdown(headers, lines[1:])
                tables.append(text)
        doc.close()

        return tables

    def _output_to_markdown(self, headers, rows):
        headers_row = [" " if cell in [None, ""] else cell for cell in headers]
        markdown_output = (
            "| " + " | ".join("%s" % i for i in headers_row) + " |"
        ).replace("\n", "")
        markdown_output += "\n" + "|---" * len(headers) + "|\n"

        for row in rows:
            processed_row = [" " if cell in [None, ""] else cell for cell in row]
            markdown_output += ("| " + " | ".join(processed_row) + " |").replace(
                "\n", ""
            )
            markdown_output += "\n"

        return markdown_output
