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


from kubeagi_core.document_transformers.pdf2csv import PDF2CSVTransform


def test_pdf_to_csv():
    pdf_transformer = PDF2CSVTransform(
        file_path="data/test.pdf",
        llm_config={
            "model": "6ac7baa2-71e7-4ffc-bd49-9356e743ecbb",
            "base_url": "http://fastchat-api.172.22.96.167.nip.io/v1",
            "api_key": "fake",
            "type": "openai",
            "temperature": "0.7",
            "max_tokens": "2048",
        },
        data_clean_config=[
            {"type": "chinese_convert"},
            {"type": "remove_emojis"},
            {"type": "remove_email", "repl": "<EMAIL>"},
            {"type": "remove_ip_address", "repl": "<IP>"},
            {"type": "remove_phone", "repl": "<PHONE>"},
        ],
        output_dir="data",
    )
    pdf_transformer.transform()
    print("<<< Finished")


if __name__ == "__main__":
    test_pdf_to_csv()
