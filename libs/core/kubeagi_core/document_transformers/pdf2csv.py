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


import csv
import logging
import os

from typing import Any, Dict, List
from pathlib import Path

from kubeagi_core.document_chunks.spacy_splitter import SpacySplitter
from kubeagi_core.document_loaders import PDFLoader
from .transform import Clean, DataConvert, FixUnicode
from kubeagi_core.qa_provider.openai import QAProviderOpenAI
from kubeagi_core.qa_provider.zhipuai import QAProviderZhiPuAIOnline

logger = logging.getLogger(__name__)


class PDF2CSVTransform:
    """
    pdf to csv transform.

    Args:
        file_path: file path.
        llm_config: llm config for generate qa.
            model: model name to use.
            base_url: base URL path for API requests.
            api_key: llm api key.
            type: llm type.
            temperature
            top_p
            max_tokens
            prompt_template
            retry_count: the number of retries when LLM model invocation fails.
            retry_wait_seconds: the waiting time between each retry when invoking the model.
        data_cleaning_config: data processing clean config.
            type: what type of data processing.
                NOTE: including the following types
                    remove_invisible_characters
                    space_standardization
                    fix_unicode
                    chinese_convert
                    remove_html_tag
                    remove_emojis
                    remove_email
                    remove_ip_address
                    remove_phone
                    remove_id_card
                    remove_weixin
                    remove_bank_card
            repl: the replacement values for the data to be processed.
        output_dir: file output path.
        chunk_size: chunk size.
        chunk_overlap: chunk overlap.
    """

    def __init__(
        self,
        file_path: str,
        llm_config: Dict[str, Any],
        data_cleaning_config: List[Dict[str, Any]] = None,
        output_dir: str = None,
        chunk_size: int = None,
        chunk_overlap: int = None,
    ):
        if chunk_size is None:
            chunk_size = 500
        if chunk_overlap is None:
            chunk_overlap = 50
        if output_dir is None:
            output_dir = os.path.dirname(file_path)
        if data_cleaning_config is None:
            data_cleaning_config = []

        self._file_path = file_path
        self._llm_config = llm_config
        self._data_cleaning_config = data_cleaning_config
        self._output_dir = output_dir
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap

    def transform(self):
        logger.info("start pdf transform csv")
        # Text splitter
        pdf_loader = PDFLoader(file_path=self._file_path)
        docs = pdf_loader.load()

        text_splitter = SpacySplitter(
            separator="\n\n",
            pipeline="zh_core_web_sm",
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
        )
        documents = text_splitter.split_documents(docs)

        res = self._data_transform(documents)
        if res.get("status") != 200:
            return res

        # save qa list for csv
        qa_data_dict = [["q", "a", "file_name", "page_number", "chunk_content"]]
        qa_data_dict.extend(res.get("data"))

        path = Path(self._file_path)
        file_name_without_extension = path.stem
        file_name = file_name_without_extension + ".csv"
        output_file_path = self._output_dir + "/" + file_name
        logger.info(f"file output path {output_file_path}")

        with open(output_file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(qa_data_dict)

        return {"status": 200, "message": "", "data": qa_data_dict}

    def _data_transform(self, documents):
        logger.info("start data cleaning")
        qa_list = []
        for document in documents:
            content = document.page_content.replace("\n", "")

            if len(self._data_cleaning_config) > 0:
                # remove invisible characters
                invisible_characters_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_invisible_characters"
                ]
                if invisible_characters_item:
                    content = DataConvert().invisible_characters_convert(
                        text=content, repl=invisible_characters_item[0].get("repl", "")
                    )

                # process for nonstandard space
                space_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "space_standardization"
                ]
                if space_item:
                    content = DataConvert().space_convert(
                        text=content, repl=space_item[0].get("repl", " ")
                    )

                # fix unicode
                unicode_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "fix_unicode"
                ]
                if unicode_item:
                    content = FixUnicode().process(text=content)

                # process for Traditional Chinese to Simplified Chinese
                chinese_convert_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "chinese_convert"
                ]
                if chinese_convert_item:
                    content = DataConvert().chinese_convert(text=content)

                # process for clean html code in text
                html_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_html_tag"
                ]
                if html_item:
                    content = Clean().clean_html(text=content)

                # process for remove emojis in text
                emoji_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_emojis"
                ]
                if emoji_item:
                    content = DataConvert().emojis_convert(
                        text=content, repl=space_item[0].get("repl", "")
                    )

                # process for remove email in text
                email_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_email"
                ]
                if email_item:
                    content = DataConvert().email_convert(
                        text=content, repl=email_item[0].get("repl", "xxxx")
                    )

                # process for remove ip addresses in text
                ip_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_ip_address"
                ]
                if ip_item:
                    content = DataConvert().ip_convert(
                        text=content, repl=ip_item[0].get("repl", "xxxx")
                    )

                # process for remove phone in text
                phone_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_phone"
                ]
                if phone_item:
                    content = DataConvert().phone_convert(
                        text=content, repl=phone_item[0].get("repl", "xxxx")
                    )

                # process for remove id card in text
                id_card_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_id_card"
                ]
                if id_card_item:
                    content = DataConvert().id_card_convert(
                        text=content, repl=id_card_item[0].get("repl", "xxxx")
                    )

                # process for remove weixin in text
                weixin_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_weixin"
                ]
                if weixin_item:
                    content = DataConvert().weixin_convert(
                        text=content, repl=weixin_item[0].get("repl", "xxxx")
                    )

                # process for remove bank card in text
                bank_card_item = [
                    item
                    for item in self._data_cleaning_config
                    if item.get("type") == "remove_bank_card"
                ]
                if bank_card_item:
                    content = DataConvert().bank_card_convert(
                        text=content, repl=bank_card_item[0].get("repl", "xxxx")
                    )

            # generate qa
            logger.info("start generate qa")
            llm_type = self._llm_config.get("type")
            if llm_type == "openai":
                # generate QA list by openai
                qa_provider = QAProviderOpenAI(
                    api_key=self._llm_config.get("api_key"),
                    base_url=self._llm_config.get("base_url"),
                    model=self._llm_config.get("model"),
                    temperature=self._llm_config.get("temperature"),
                    max_tokens=self._llm_config.get("max_tokens"),
                )
            elif llm_type == "zhipuai":
                # generate QA list by zhipuai
                qa_provider = QAProviderZhiPuAIOnline(
                    api_key=self._llm_config.get("api_key"),
                    model=self._llm_config.get("model"),
                    temperature=self._llm_config.get("temperature"),
                    top_p=self._llm_config.get("top_p"),
                )
            else:
                return {"status": 1000, "message": "暂时不支持该类型的模型", "data": ""}

            data = qa_provider.generate_qa_list(
                text=content,
                prompt_template=self._llm_config.get("prompt_template"),
                retry_count=self._llm_config.get("retry_count"),
                retry_wait_seconds=self._llm_config.get("retry_wait_seconds"),
            )
            if data.get("status") != 200:
                return data

            for qa in data.get("data"):
                qa_list.append(
                    [
                        qa[0],
                        qa[1],
                        document.metadata.get("source"),
                        document.metadata.get("page"),
                        document.page_content.replace("\n", ""),
                    ]
                )
        logger.info("generate qa finished")

        return {"status": 200, "message": "", "data": qa_list}
