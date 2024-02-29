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
import re
import time
import traceback

from kubeagi_core.qa_provider.base import BaseQAProvider
from kubeagi_core.qa_provider.prompt import PROMPT_TEMPLATE
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate

logger = logging.getLogger(__name__)


class QAProviderOpenAI(BaseQAProvider):
    """The QA provider is used by open ai."""

    def __init__(self, api_key, base_url, model, temperature=None, max_tokens=None):
        if temperature is None:
            temperature = 0.8
        if max_tokens is None:
            max_tokens = 512

        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=float(temperature),
            max_tokens=int(max_tokens),
        )

    def generate_qa_list(
        self, text, prompt_template=None, retry_count=None, retry_wait_seconds=None
    ):
        """Generate the QA list.

        Parameters
        ----------
        text
            use the text to generate QA list
        prompt_template
            the prompt template
        retry_count
            number of retries
        retry_wait_seconds
            wait time per retry
        """
        if prompt_template is None:
            prompt_template = PROMPT_TEMPLATE
        if retry_count is None:
            retry_count = 3
        if retry_wait_seconds is None:
            retry_wait_seconds = 10

        human_message_prompt = HumanMessagePromptTemplate.from_template(prompt_template)
        prompt = ChatPromptTemplate.from_messages([human_message_prompt])
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)

        result = []
        status = 200
        message = ""
        invoke_count = 0
        while True:
            try:
                if invoke_count >= int(retry_count):
                    logger.error(
                        "".join(
                            [
                                f"Cannot access the open ai service.\n",
                                f"The tracing error is: \n{traceback.format_exc()}\n",
                            ]
                        )
                    )

                    status = 1000
                    break

                response = llm_chain.invoke(input=text)
                result = self.__get_qa_list_from_response(response.get("text"))
                if len(result) > 0:
                    break

                logger.warn("failed to get QA list, wait for 10 seconds and retry")
                time.sleep(retry_wait_seconds)  # sleep 10 seconds
                invoke_count += 1
                message = "模型调用成功，生成的QA格式不对，请更换prompt"
            except Exception as ex:
                time.sleep(retry_wait_seconds)
                invoke_count += 1
                message = "调用本地模型失败，请检查模型是否可用"

        return {"status": status, "message": message, "data": result}

    def __get_qa_list_from_response(self, response):
        """Get the QA list from the response.

        Notice: There are some problems in the local OpenAI service.
        Some time it cannot return the correct question and answer list.

        Parameters
        ----------
        response
            the response from open ai service
        """
        result = []
        try:
            pattern = re.compile(r"Q\d+:(\s*)(.*?)(\s*)A\d+:(\s*)([\s\S]*?)(?=Q|$)")

            # 移除换行符
            response_text = response.replace("\\n", "")
            matches = pattern.findall(response_text)

            for match in matches:
                q = match[1]
                a = match[4]
                if q and a:
                    a = re.sub(r"[\n]", "", a).strip()
                    result.append([q, a])
        except Exception as ex:
            logger.error(
                "".join(
                    [
                        f"从结果中提取QA失败\n",
                        f"The tracing error is: \n{traceback.format_exc()}\n",
                    ]
                )
            )

        return result
