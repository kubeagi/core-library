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


from typing import List
from FlagEmbedding import FlagReranker
from BCEmbedding import RerankerModel
from abc import ABC, abstractmethod


class BaseReranking(ABC):
    """
    The Reranking is used to run reranking models.
    """

    @abstractmethod
    def run(self, pairs: List[List[str]]):
        """run reranking models to rerank pairs."""


class BGEReranking(BaseReranking):
    """
    The BGEReranking is used to run reranking models with FlagEmbedding like sbge-reranker-large(https://huggingface.co/BAAI/bge-reranker-large)
    """

    _reranker: FlagReranker

    def __init__(
        self,
        model_name_or_path: str,
    ):
        self._reranker = FlagReranker(
            model_name_or_path=model_name_or_path, use_fp16=False
        )

    # run bge reranking model
    def run(self, pairs: List[List[str]]):
        if len(pairs) > 0:
            result = self._reranker.compute_score(pairs)
            if isinstance(result, float):
                result = [result]
            return result
        else:
            return None


class BCEReranking(BaseReranking):
    """
    The BGEReranking is used to run reranking models with BCEEmbedding from https://github.com/netease-youdao/BCEmbedding
    """

    _reranker: RerankerModel

    def __init__(
        self,
        model_name_or_path: str,
    ):
        self._reranker = RerankerModel(
            model_name_or_path=model_name_or_path, use_fp16=False
        )

    # run bge reranking model
    def run(self, pairs: List[List[str]]):
        if len(pairs) > 0:
            result = self._reranker.compute_score(pairs)
            if isinstance(result, float):
                result = [result]
            return result
        else:
            return None


def select_reranking(model_name_or_path: str) -> BaseReranking:
    if "bge" in model_name_or_path.lower():
        return BGEReranking(model_name_or_path)
    if "bce" in model_name_or_path.lower():
        return BCEReranking(model_name_or_path)

    raise ValueError(f"No valid reranking runner for {model_name_or_path}")
