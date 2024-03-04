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


from langchain_community.embeddings import OpenAIEmbeddings
from typing import List


class OpenAIEmbedding:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
    ):
        """OpenAI embedding models.

        Args:
            base_url (str): to support OpenAI Service custom endpoints.
            api_key (str): to support OpenAI Service API KEY.
            model (str): Embeddings Model.
        """
        self._embeddings = OpenAIEmbeddings(
            api_key=api_key,
            base_url=base_url,
            model=model,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._embeddings.embed_documents(texts=texts)

    def embed_query(self, text: str) -> List[float]:
        return self._embeddings.embed_query(text=text)
