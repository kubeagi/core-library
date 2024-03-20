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


import typer

from typing import List
from typing_extensions import Annotated

convert_cli = typer.Typer(no_args_is_help=True, add_completion=False)


@convert_cli.command()
def pdf(
    file_path: Annotated[
        str,
        typer.Argument(
            help="file path",
        ),
    ] = None,
    llm_config: Annotated[
        str,
        typer.Argument(
            help="llm config for generate qa",
        ),
    ] = None,
    data_cleaning_config: Annotated[
        List[str],
        typer.Option(help="data cleaning config"),
    ] = [],
    output_dir: Annotated[
        str,
        typer.Option(help="file output path"),
    ] = None,
    chunk_size: Annotated[
        int,
        typer.Option(help="text chunk size"),
    ] = 500,
    chunk_overlap: Annotated[
        int,
        typer.Option(help="text chunk overlap"),
    ] = 50,
):
    import ujson
    from kubeagi_core.document_transformers.pdf2csv import PDF2CSVTransform

    """
    pdf transformer csv.
    """
    if len(data_cleaning_config) > 0:
        data_cleaning_config = [ujson.loads(s) for s in data_cleaning_config]

    pdf_transformer = PDF2CSVTransform(
        file_path=file_path,
        llm_config=ujson.loads(llm_config),
        data_cleaning_config=data_cleaning_config,
        output_dir=output_dir,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return pdf_transformer.transform()
