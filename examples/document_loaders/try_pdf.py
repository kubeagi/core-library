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

from kubeagi_core.document_loaders import PDFLoader


def test_load_pdf():
    print(">>> Starting load pdf")
    pdf_loader = PDFLoader(file_path="xxx.pdf")

    document = pdf_loader.load()
    print("<<< Finished")
    print(f"document: {document}")


def test_extract_images(file_path, output_dir):
    print(">>> Starting extract images for pdf")
    pdf_loader = PDFLoader(file_path=file_path)

    loader.extract_images(output_dir=output_dir, remove_small_images=True)
    print("<<< Finished")
    print(f"images output dir: {output_dir}")


if __name__ == "__main__":
    test_load_pdf()
