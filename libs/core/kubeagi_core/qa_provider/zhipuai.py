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

import zhipuai

from kubeagi_core.qa_provider.prompt import PROMPT_TEMPLATE
from kubeagi_core.qa_provider.base import BaseQAProvider

logger = logging.getLogger(__name__)


class QAProviderZhiPuAIOnline(BaseQAProvider):
    """The QA provider is used by zhi pu ai online."""

    def __init__(self, api_key, model, temperature=None, top_p=None):
        if top_p is None:
            self._top_p = 0.7
        if temperature is None:
            self._temperature = 0.8
        self._model = model

        zhipuai.api_key = api_key

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
            retry_wait_seconds = 120

        content = prompt_template.format(text=text)

        result = []
        status = 200
        message = ""

        invoke_count = 0
        while True:
            logger.debug("".join([f"content.\n", f"{content}\n"]))
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

                response = zhipuai.model_api.invoke(
                    model=self._model,
                    prompt=[{"role": "user", "content": content}],
                    top_p=float(self._top_p),
                    temperature=float(self._temperature),
                )
                if response["success"]:
                    result = self.__format_response_to_qa_list(response)
                    if len(result) > 0:
                        break

                    logger.warn(
                        f"failed to get QA list, wait for {retry_wait_seconds} seconds and retry"
                    )
                    time.sleep(retry_wait_seconds)  # sleep 120 seconds
                    invoke_count += 1
                    message = "模型调用成功，生成的QA格式不对，请更换prompt"
                else:
                    logger.error(
                        "".join(
                            [
                                f"Cannot access the ZhiPuAI service.\n",
                                f"The error is: \n{response['msg']}\n",
                            ]
                        )
                    )
                    logger.warn(
                        f"zhipuai request failed, wait for {retry_wait_seconds} seconds and retry"
                    )
                    time.sleep(retry_wait_seconds)  # sleep 120 seconds
                    invoke_count += 1
                    message = "模型调用失败，失败原因: " + response["msg"]
            except Exception as ex:
                logger.warn(
                    f"zhipuai request exception, wait for {retry_wait_seconds} seconds and retry"
                )
                time.sleep(retry_wait_seconds)
                invoke_count += 1
                message = "模型调用失败，请检查模型是否可用！"

        return {"status": status, "message": message, "data": result}

    def __format_response_to_qa_list(self, response):
        """Format the response to the QA list."""
        text = response["data"]["choices"][0]["content"]
        result = []
        try:
            pattern = re.compile(r"Q\d+:(\s*)(.*?)(\s*)A\d+:(\s*)([\s\S]*?)(?=Q|$)")
            # 移除换行符
            text = text.replace("\\n", "")
            matches = pattern.findall(text)

            for match in matches:
                q = match[1]
                a = match[4]
                if q and a:
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
