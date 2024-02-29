# kubeagi-cli
This package implements the CLI for Kubeagi Core.

## Quick Start

There are several ways to use the `kubeagi-cli` library:
* Install the library
    1. [Install from PyPI](https://github.com/kubeagi/core-library/tree/main/libs/core/cli#installing-the-library)

### Installing the library
Use the following instructions to get up and running with `kubeagi-cli` and test your
installation.

- Install the Python SDK `pip install kubeagi-cli`

At this point, you should be able to run the following code:

```shell
convert -v
```

## Commands

### RAG Evaluation

```shell
kubeagi-cli evaluate --help

 Usage: kubeagi-cli evaluate [OPTIONS] [METRICS] [DATASET]                                                                                                                                                
                                                                                                                                                                                                     
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   metrics      [METRICS]  Specifies the metrics to use for evaluation. Comma-separated values. [default: ragas.csv]                                                                               │
│   dataset      [DATASET]  Specifies the path to the dataset for evaluation. [default: ragas.csv]                                                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --apibase                  TEXT  The base URL for the API. Defaults to OpenAI. [default: https://api.openai.com/v1]                                                                               │
│ --apikey                   TEXT  Specifies the API key to authenticate requests. [default: fake]                                                                                                  │
│ --llm-model                TEXT  Specifies the model to use for evaluation. [default: gpt-3.5-turbo.]                                                                                             │
│ --embedding-apibase        TEXT  Specifies the base URL for the Embedding API. Defaults to OpenAI. [default: https://api.openai.com/v1]                                                           │
│ --embedding-apikey         TEXT  Specifies the API key for the Embedding API to authenticate requests. [default: fake]                                                                             │
│ --embedding-model          TEXT  Specifies embeddings model (or its path) to use for evaluation. [default: text-embedding-ada-002]                                                                │
│ --output-dir               TEXT  Specifies the output directory to store the evaluation results [default: None]                                                                                    │
│ --help                           Show this message and exit.                                                                                                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

For example:

```shell
kubeagi-cli evaluate context_precision ~/core-library/examples/testdata/ragas.csv
```

The above command will run the rag evaluation with metrics `context_precision` and test dataset `~/core-library/examples/testdata/ragas.csv` with the help 
of OpenAI.