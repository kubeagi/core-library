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

from kubeagi_core.document_chunks.spacy_splitter import SpacySplitter
from kubeagi_core.document_loaders import PDFLoader


def test_spacy_text_splitter():
    print(">>> Starting spacy text splitter")
    pdf_loader = PDFLoader(file_path="xxx.pdf")
    pdf_documents = pdf_loader.load()

    splitter = SpacySplitter(
        separator="\n\n",
        pipeline="zh_core_web_sm",
        chunk_size=100,
        chunk_overlap=10,
    )
    documents = splitter.split_documents(pdf_documents)

    print("<<< Finished")
    print(f"document: {documents}")


if __name__ == "__main__":
    test_spacy_text_splitter()
