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

import os
from typing import Optional, List
from fastapi import FastAPI

from pydantic import BaseModel, Field
from kubeagi_cli.serve.reranking import select_reranking

webapp = FastAPI()


@webapp.get("/api/v1/health")
def health():
    return {"Health": True}


class RerankingInput(BaseModel):
    model_name_or_path: Optional[str] = Field(default=os.getenv("RERANKING_MODEL_PATH"))
    question: str
    answers: Optional[List[str]]


@webapp.post("/api/v1/reranking")
def reranking(input: RerankingInput):
    # select reranking models based on model path
    reranker = select_reranking(input.model_name_or_path)
    # prepare reranking pairs
    pairs = []
    for answer in input.answers:
        pairs.append([input.question, answer])
    return reranker.run(pairs)
