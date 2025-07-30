
<div align="center">
  <img src="docs/assets/img/ragformance_banner.png" alt="RAGFORmance : Benchmark generators for RAG">
<br/>
  <!-- Link to the documentation -->
  <a href="TODO"><strong>Explore RAGFORmance docs »</strong></a>
  <br>

</div>

[![Build status](https://github.com/FOR-sight-ai/RAGFORmance/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/FOR-sight-ai/ragformance/actions)
[![Docs status](https://img.shields.io/readthedocs/RAGFORmance)](TODO)
[![Version](https://img.shields.io/pypi/v/ragformance?color=blue)](https://pypi.org/project/ragformance/)
[![Python Version](https://img.shields.io/pypi/pyversions/ragformance.svg?color=blue)](https://pypi.org/project/ragformance/)
[![Downloads](https://static.pepy.tech/badge/ragformance)](https://pepy.tech/project/ragformance)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/FOR-sight-ai/ragformance/blob/main/LICENSE)

# Installation

Install the library using pip: `pip install ragformance` or preferably using uv: `uv sync`

# Usage

## Running the RAGformance Pipeline (including Data Generation)

The primary way to use RAGformance, including its data generation capabilities, is through the command-line interface (CLI) with a configuration file.

`ragformance --config your_config.json`

### Configuring Data Generators

Data generation is controlled via the `generation` section within your `your_config.json` file. You need to specify the `type` of generator and provide necessary parameters.

**Example `config.json` snippet for data generation:**
```json
{
  "LLMs": [ // Define your LLMs here, used by generators & RAG
    {
      "name": "default_llm",
      "provider": "openai", // or "ollama", "openrouter", etc.
      "model": "gpt-3.5-turbo",
      "api_key": "YOUR_API_KEY_OR_ENV_VAR_NAME", // Can be actual key or ENV_VAR name
      "base_url": "YOUR_BASE_URL_IF_NEEDED"
      // Specific params for this LLM can go into a "params" object here
    }
    // Potentially other LLM configurations
  ],
  "embeddings": [ // Define your embedding models
    {
      "name": "default_embedding",
      "provider": "openai", // or "huggingface", etc.
      "model": "text-embedding-ada-002",
      "api_key": "YOUR_API_KEY_OR_ENV_VAR_NAME" // Can be actual key or ENV_VAR name
      // Specific params for this embedding model can go into a "params" object here
    }
  ],
  // ... other global settings ...

  "generation": {
    "type": "alpha", // Or "aida", "ragas", "error_code", etc.
    "source": {
      "path": "path/to/your/input_data" // Folder or specific file depending on generator
    },
    "output": {
      "path": "path/to/your/output_folder" // Where corpus.jsonl, queries.jsonl will be saved
    },
    "params": {
      // Generator-specific parameters. Examples:
      // For "alpha":
      //   "temporary_folder": "temp/alpha_conversion",
      // For "error_code":
      //   "corpus_id_prefix": "ERR",
      //   "document_title": "System Manual",
      //   "data_file_name": "error_codes_chapter.md"
      // For "tokenburner":
      //   "pdf_path": "path/to/specific.pdf", // If different from generation.source.path
      //   "categories_file_path": "config/tokenburner_categories.txt",
      //   "user_queries": ["What is X?", "How to fix Y?"]
    }
  },

  // For complex generators like AIDA or RAGAS, you might also need
  // dedicated top-level configuration blocks, e.g.:
  // "aida_generator_config": { /* AIDA specific detailed settings */ },
  // "ragas_generator_config": { /* RAGAS specific detailed settings */ },

  "steps": { // Control which parts of the pipeline run
    "generation": true, // Set to true to run data generation
    "upload_hf": false,
    "evaluation": true,
    // ... other steps
  }
}
```

For detailed information on available generators, their specific parameters, and advanced configuration (especially for AIDA and RAGAS), please refer to the [**Generators Documentation**](ragformance/generators/README.md).

The generated dataset (typically `corpus.jsonl` and `queries.jsonl`) will be saved to the specified `generation.output.path`.

### Dataset Structure
The dataset consists of two files:
- `corpus.jsonl`: A jsonl file containing the corpus of documents. Each document is represented as a json object with the following fields:
    - `_id`: The id of the document.
    - `title`: The title of the document.
    - `text`: The text of the document.
- `queries.jsonl`: A jsonl file containing the queries. Each query is represented as a json object with the following fields:
    - `_id`: The id of the query.
    - `query_text`: The text of the query.
    - `relevant_document_ids`: A list of references to the documents in the corpus. Each reference is represented as a json object with the following fields:
        - `corpus_id`: The id of the document.
        - `score`: The score of the reference.
    - `ref_answer`: The reference answer for the query.
    - `metadata`: A dictionary containing the metadata for the query.

This structure is inspired by the popular BEIR format, with the inclusion of the `qrels`file inside the queries : indeed, BEIR is optimized for Information Retrieval tasks whereas this library aims also to evaluates other tasks (such as end to end generation).

## Pushing dataset to Hugging Face Hub
This function pushes the two jsonl files to a Hugging Face Hub dataset repository; you must set the environment variable HF_TOKEN, either in system environment or config.json

``` python
from ragformance.eval.utils.huggingface_dataloader import push_to_hub
HFpath = "FOR-sight-ai/ragformance_toloxa"
push_to_hub(HFpath, "output")
```


## Using test suite with BEIR datasets
This functions convert BEIR jsonl data into the internal jsonl format. They are very similar, but BEIR is only for information retrieval task, whereas the library allows other type of evaluations.

``` python
from ragformance.rag.naive_rag import NaiveRag
from ragformance.eval.utils.beir_dataloader import load_beir_dataset


import logging
import json

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
with open('config.json','w') as f:
  json.dump({},f)



corpus, queries = load_beir_dataset(filter_corpus = True)

naive_rag = NaiveRag()
doc_uploaded_num = naive_rag.upload_corpus(corpus=corpus)
answers = naive_rag.ask_queries(queries)


```


### Answer Output Format
The answers generated by the system are structured as a json lines, with each line corresponding to a processed question. Each entry contains:

- `query`: A dictionary describing the original question, with:
  - `_id`: Unique identifier for the question.
  - `query_text`: The question text.
  - `relevant_document_ids`: A list of corpus documents considered as references for this question, each reference containing:
    - `corpus_id`: The document identifier.
    - `score`: The importance or relevance score.
  - `ref_answer`: The reference (gold standard) answer for the question.
- `model_answer`: The generated answer
- `relevant_documents_ids`: A list of corpus document IDs used as context for generating the answer.
- `retrieved_documents_distances`: A list of relevancy scores for the retrieved documents.

It is based on the following pydantic model
```python
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class RelevantDocumentModel(BaseModel):
    corpus_id: str
    score: int

class AnnotatedQueryModel(BaseModel):
    id: str = Field(alias="_id")
    query_text: str

    relevant_document_ids: List[RelevantDocumentModel]
    ref_answer: str

    metadata: Optional[Dict] = None

class AnswerModel(BaseModel):
    id: str = Field(alias="_id")

    query: AnnotatedQueryModel

    # model output
    model_answer: str
    retrieved_documents_ids: List[str]
    retrieved_documents_distances: Optional[List[float]] = None
```

## Loading a dataset from Hugging face

You can use directly datasets with the correct format that are hosted on Hugging Face

``` python

from typing import List

from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel
from ragformance.rag.naive_rag import NaiveRag
from pydantic import TypeAdapter

from datasets import load_dataset
ta = TypeAdapter(List[DocModel])
taq = TypeAdapter(List[AnnotatedQueryModel])

corpus= ta.validate_python(load_dataset("FOR-sight-ai/ragformance_toloxa", "corpus", split="train))
queries = taq.validate_python(load_dataset("FOR-sight-ai/ragformance_toloxa", "queries", split="train"))

naive_rag = NaiveRag()
doc_uploaded_num = naive_rag.upload_corpus(corpus=corpus)
answers = naive_rag.ask_queries(queries)


```

## Loading a dataset from jsonl

```python
from typing import List

from ragformance.models.corpus import DocModel
from ragformance.rag.naive_rag import NaiveRag
from pydantic import TypeAdapter

ta = TypeAdapter(List[DocModel])

# load from jsonl file
with open("output/corpus.jsonl","r") as f:
    corpus= ta.validate_python([json.loads(line) for line in f])

naive_rag = NaiveRag()
doc_uploaded_num = naive_rag.upload_corpus(corpus=corpus)

```

## Metrics and visualization
This library wraps the trev eval tools for Information Retrieval metrics.
It provides also a set metrics visualization to help assess if the test dataset is well balanced and if a solution under test has the expected performances.

```python

from ragformance.eval.metrics import trec_eval_metrics
from ragformance.eval.metrics import visualize_semantic_F1, display_semantic_quadrants

metrics = trec_eval_metrics(answers)

quadrants = visualize_semantic_F1(corpus, answers)

display_semantic_quadrants(quadrants)

```

## Haystack Pipeline

> ⚠️ **Warning**  <br>
> - **Haystrack v1.22.1** is used here, which requires **Pydantic versions < 2**.  <br>
> - **Haystrack > v2** uses more recent versions of Pydantic, but there have been significant architectural changes and current codes need to be adapted. <br>
> - **Poetry** is used to tackle the dependencies (make poetry install and poetry run python your_code.py)

```python
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, RelevantDocumentModel
from ragformance.rag.haystack_rag import HaystackRAG

docs = [
    DocModel(_id="1", title="Paris", text="Paris est la capitale de la France."),
    DocModel(_id="2", title="Président", text="Emmanuel Macron est le président de la République française."),
    DocModel(_id="3", title="Langue", text="Le français est la langue officielle en France."),
]

queries = [
    AnnotatedQueryModel(
        _id="q1",
        query_text="Quelle est la capitale de la France ?",
        relevant_document_ids=[RelevantDocumentModel(corpus_id="1", score=1)],
        ref_answer="Paris"
    ),
    AnnotatedQueryModel(
        _id="q2",
        query_text="Qui est le président de la République française ?",
        relevant_document_ids=[RelevantDocumentModel(corpus_id="2", score=1)],
        ref_answer="Emmanuel Macron"
    ),
    AnnotatedQueryModel(
        _id="q3",
        query_text="Quelle est la langue officielle en France ?",
        relevant_document_ids=[RelevantDocumentModel(corpus_id="3", score=1)],
        ref_answer="Le français"
    ),
]

rag = HaystackRAG()
rag.upload_corpus(docs)
answers = rag.ask_queries(queries)

for a in answers:
    print(f"Q: {a.query.query_text}")
    print(f"A: {a.model_answer}")
    print(f"Retrieved: {a.retrieved_documents_ids}")
    print("-" * 40)
```
If you want to use a LLM instead of a simple READER, you can use Ollama via an API_ENDPOINT URL. In this case, HaystackRAG class can be instantiated like this :  
```python
rag = HaystackRAG(
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
    ollama_model="smollm2:360m-instruct-q8_0",
    ollama_url=API_ENDPOINT
)
```


## Example configuration file

``` json
{
    "corpus_text_key": "text"
}


```

## Run tests

```bash
python -m unittest
```

## Acknowledgement

This project received funding from the French ”IA Cluster” program within the Artificial and Natural Intelligence Toulouse Institute (ANITI) and from the "France 2030" program within IRT Saint Exupery. The authors gratefully acknowledge the support of the FOR projects.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
