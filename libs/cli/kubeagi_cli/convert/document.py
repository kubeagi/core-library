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

from typing import Optional

import typer
from typing_extensions import Annotated

from kubeagi_core.document_loaders import PDFLoader

document_cli = typer.Typer(no_args_is_help=True, add_completion=False)


@document_cli.command()
def pdf_load(
    file_path: Annotated[
        Optional[str],
        typer.Argument(
            help="The file path",
        ),
    ] = None,
):
    """
    Load and return all Documents from the pdf file.
    """
    pdf_loader = PDFLoader(file_path=file_path)

    documents = pdf_loader.load()
    typer.echo(documents)
    return documents
