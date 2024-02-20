# Kubeagi Core
Kubeagi Core including some common functions, these functions are designed to be as modular and simple as possible.

## Quick Start

There are several ways to use the `kubeagi_core` library:
* Install the library
    1. [Install from PyPI](https://github.com/kubeagi/core-library/libs/core/kubeagi_core#installing-the-library)

### Installing the library
Use the following instructions to get up and running with `kubeagi_core` and test your
installation.

- Install the Python SDK `pip install kubeagi_core`

At this point, you should be able to run the following code:

```python
from kubeagi_core.qa_provider.openai import QAProviderOpenAI

qa_provider = QAProviderOpenAI(
    api_key="fake",
    base_url="http://fastchat-api.172.22.95.167.nip.io/v1",
    model="f8e35823-3841-4253-ae79-0fff47917ae3",
)

data = qa_provider.generate_qa_list(text="大语言模型（LLM）是指使用大量文本数据训练的深度学习模型，可以生成自然语言文本或理解语言文本的含义。大语言模型可以处理多种自然语言任务，如文本分类、问答、对话等，是通向人工智能的一条重要途径。")

print(data)
```