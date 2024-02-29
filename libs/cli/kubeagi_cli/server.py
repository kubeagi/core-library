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

from pydantic import BaseModel
from serve.reranking import Reranking

app = FastAPI()


@app.get("/api/v1/health")
def health():
    return {"Health": True}


class RerankingInput(BaseModel):
    question: str
    answers: Optional[List[str]]


@app.post("/api/v1/reranking")
def reranking(input_docs: RerankingInput):
    pairs = []
    for answer in input_docs.answers:
        pairs.append([input_docs.question, answer])
    reranker = Reranking(model_path=os.getenv("RERANKING_MODEL_PATH"))
    return reranker.run(pairs)
