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


class Reranking:
    """
    The Reranking is used to run reranking models like bge-reranker-large(https://huggingface.co/BAAI/bge-reranker-large)
    """

    _model_path: str
    _reranker: FlagReranker

    def __init__(
        self,
        model_path: str,
    ):
        self._model_path = model_path

    def run(self, pairs: List[List[str]]):
        reranker = FlagReranker(self._model_path, use_fp16=False)
        if len(pairs) > 0:
            result = reranker.compute_score(pairs)
            if isinstance(result, float):
                result = [result]
            return result
        else:
            return None
