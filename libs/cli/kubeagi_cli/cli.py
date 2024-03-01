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
import typer
from typing_extensions import Annotated
from kubeagi_core.evaluation.ragas_eval import RagasEval
from kubeagi_cli.convert import document as convert_document


__version__ = "0.0.1"

app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(
    convert_document.document_cli,
    name="convert_document",
    help=convert_document.__doc__,
)


@app.command()
def serve(
    host: Annotated[
        str,
        typer.Option(
            help="The base URL for the API. Defaults to OpenAI.",
        ),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option(
            help="The base URL for the API. Defaults to OpenAI.",
        ),
    ] = 8000,
):
    import uvicorn

    uvicorn.run("server:app", host=host, port=port, reload=True)


@app.command()
def evaluate(
    metrics: Annotated[
        str,
        typer.Argument(
            help="Specifies the metrics to use for evaluation. Comma-separated values.",
        ),
    ] = "ragas.csv",
    dataset: Annotated[
        str,
        typer.Argument(
            help="Specifies the path to the dataset for evaluation.",
        ),
    ] = "ragas.csv",
    apibase: Annotated[
        str,
        typer.Option(
            help="The base URL for the API. Defaults to OpenAI.",
        ),
    ] = "https://api.openai.com/v1",
    apikey: Annotated[
        str,
        typer.Option(
            help="Specifies the API key to authenticate requests.",
        ),
    ] = "fake",
    llm_model: Annotated[
        str,
        typer.Option(
            help="Specifies the model to use for evaluation.",
        ),
    ] = "gpt-3.5-turbo.",
    embedding_apibase: Annotated[
        str,
        typer.Option(
            help="Specifies the base URL for the Embedding API. Defaults to OpenAI.",
        ),
    ] = "https://api.openai.com/v1",
    embedding_apikey: Annotated[
        str,
        typer.Option(
            help="Specifies the API key for the Embedding API to authenticate requests.",
        ),
    ] = "fake",
    embedding_model: Annotated[
        str,
        typer.Option(
            help="Specifies embeddings model (or its path) to use for evaluation.",
        ),
    ] = "text-embedding-ada-002",
    output_dir: Annotated[
        str,
        typer.Option(
            help="Specifies the output directory to store the evaluation results",
        ),
    ] = None,
):
    print("evaluate RAG(Retrieval Augmented Generation)")
    # Initialize ragas_once with provided arguments
    eval = RagasEval(
        api_base=apibase,
        api_key=apikey,
        llm_model=llm_model,
        embedding_api_base=embedding_apibase,
        embedding_api_key=embedding_apikey,
        embedding_model=embedding_model,
    )

    # Run the evaluation
    try:
        result = eval.evaluate(dataset, metrics.split(","))
    except Exception as e:
        print("An error occurred during evaluation:", str(e))
        return

    if output_dir == None:
        output_dir = os.getcwd()
    print(f"output evaluation results to {output_dir}")
    # count total score and avearge
    summary = result.scores.to_pandas().mean()
    summary["total_score"] = summary.mean()
    summary.to_csv(output_dir + "/summary.csv")
    result.to_pandas().to_csv(output_dir + "/result.csv")


def version_callback(show_version: bool) -> None:
    if show_version:
        typer.echo(f"kubeagi-cli {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Print the current CLI version.",
        callback=version_callback,
        is_eager=True,
    ),
):
    pass


if __name__ == "__main__":
    app()
