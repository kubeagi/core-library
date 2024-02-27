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

from kubeagi_core.qa_provider.openai import QAProviderOpenAI
from kubeagi_core.qa_provider.zhipuai import QAProviderZhiPuAIOnline


def test_qa_provider_by_open_ai():
    print(">>> Starting generate qa by open ai")
    qa_provider = QAProviderOpenAI(
        api_key="fake",
        base_url="http://fastchat-api.172.22.96.167.nip.io/v1",
        model="f8e35823-3841-4253-ae79-0fff47917fb3",
        temperature=0.8,
        max_tokens=512,
    )

    data = qa_provider.generate_qa_list(
        text="大语言模型（LLM）是指使用大量文本数据训练的深度学习模型，可以生成自然语言文本或理解语言文本的含义。大语言模型可以处理多种自然语言任务，如文本分类、问答、对话等，是通向人工智能的一条重要途径。天"
    )

    print("<<< Finished")
    print(f"QA data: {data}")


def test_qa_provider_by_zhipu_ai():
    print(">>> Starting generate qa by zhipu ai")
    qa_provider = QAProviderZhiPuAIOnline(
        api_key="fake",
        model="",
        temperature=0.8,
    )

    data = qa_provider.generate_qa_list(
        text="大语言模型（LLM）是指使用大量文本数据训练的深度学习模型，可以生成自然语言文本或理解语言文本的含义。大语言模型可以处理多种自然语言任务，如文本分类、问答、对话等，是通向人工智能的一条重要途径。"
    )

    print("<<< Finished")
    print(f"QA data: {data}")


if __name__ == "__main__":
    test_qa_provider_by_open_ai()
    test_qa_provider_by_zhipu_ai()
