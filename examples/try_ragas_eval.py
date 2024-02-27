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

from kubeagi_core.evaluation.ragas_eval import RagasEval


def main():
    evaluation = RagasEval(
        api_base="http://fastchat-api.172.22.96.167.nip.io/v1",
        api_key="fake",
        llm_model="f8e35823-3841-4253-ae79-0fff47917fb3",
        embedding_model="ccb8e2eb-26f1-43b4-9bcf-b88d0c359992",
    )

    # Prepare the dataset
    dataset = evaluation.prepare_dataset("testdata/ragas.csv")

    if dataset is None:
        raise ValueError("No dataset provided")

    metrics_list = [
        "answer_relevancy",
        "context_precision",
        "context_recall",
        "context_relevancy",
        "faithfulness",
    ]

    # Get the metrics to evaluate
    metrics = evaluation.get_ragas_metrics(metrics_list)

    # Run the evaluation
    result = evaluation.evaluate(dataset=dataset, metrics=metrics)

    print(result)
