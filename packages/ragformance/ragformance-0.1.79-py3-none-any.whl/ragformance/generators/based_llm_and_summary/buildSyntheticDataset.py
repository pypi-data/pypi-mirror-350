#!/usr/bin/env python3
"""
Build the two-file dataset required by BEIR-style benchmarks:

corpus.jsonl  :
    {"_id": str, "title": str, "text": str}

queries.jsonl :
    {"_id": str,
     "text": str,
     "references": [{"corpus_id": str, "score": float}],
     "ref_answer": str,
     "metadata": {...}}
"""

# ────────────────────────────── Imports ────────────────────────────────────
import os
import re
import json
import yaml
import logging
from datetime import datetime
from dotenv import load_dotenv
import litellm

# ─────── Load all variables from .env file, overwriting existing ones ───────
# load_dotenv(dotenv_path=".env", override=True) # Removed: Generator will handle config

# ────────────────────────  Logging setup  ──────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


# ──────────────────────  Network / Proxy setup  ────────────────────────────
def set_proxy_environment() -> None:
    """
    Set proxy, no_proxy, and CA bundle env vars from the environment.
    """
    proxy = os.environ.get("PROXY", "")
    no_proxy = os.environ.get("NO_PROXY", "")
    ca_bundle = os.environ.get("CA_BUNDLE")

    if proxy:
        for key in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
            os.environ[key] = proxy
    if no_proxy:
        os.environ["NO_PROXY"] = no_proxy
        os.environ["no_proxy"] = no_proxy

    os.environ["CURL_CA_BUNDLE"] = ca_bundle
    os.environ["REQUESTS_CA_BUNDLE"] = ca_bundle
    os.environ["SSL_CERT_FILE"] = ca_bundle
    os.environ["OPENAI_LOG"] = "info"


# Decide whether to set proxy based on USE_PROXY variable
# use_proxy = os.environ.get("USE_PROXY", "false").lower() == "true" # Removed

# if use_proxy: # Removed
    # set_proxy_environment() # Removed

# ─────── Decide whether to set proxy based on USE_PROXY env var ───────
# use_proxy = os.environ.get("USE_PROXY", "false").lower() == "true" # Removed

# if use_proxy: # Removed
    # set_proxy_environment() # Removed

# ─────────────────────────── External libs ─────────────────────────────────
try:
    from unstructured.partition.auto import partition
except ImportError as err:
    logger.error(
        "Package 'unstructured[md,pdf]' missing:  pip install " "'unstructured[md,pdf]'"
    )
    raise err


# ────────────────────────  OpenAI configuration  ───────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_SUM_MODEL = os.getenv("OPENAI_SUMMARY_MODEL")
OPENAI_QA_MODEL = os.getenv("OPENAI_QA_MODEL")

# No global client initialization needed for litellm in this context,
# API key and base URL will be passed directly to litellm.completion calls.

# ───────────────────────────  Helpers ──────────────────────────────────────
def extract_contents(file_path: str) -> str:
    """Extract raw text from an arbitrary file with unstructured."""
    try:
        elements = partition(file_path)
        return "\n".join(e.text for e in elements if getattr(e, "text", ""))
    except Exception as exc:
        logger.error("Failed to extract from %s : %s", file_path, exc)
        return ""


def create_summary(text: str) -> str:
    """Ask the LLM for a concise markdown summary."""
    try:
        response = litellm.completion(
            model=OPENAI_SUM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Write a concise markdown summary:\n\n" + text,
                }
            ],
            temperature=0.3,
            top_p=0.9,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
        )
        return response.choices[0].message.content.strip()
    except Exception as err: # General exception for litellm errors
        logger.error("Summary generation error: %s", err)
        return ""


# Safer system prompt: *no* context field, only the needed list
SYSTEM_PROMPT = """
You will receive a short text (summary of a document).
1. Produce 10 diverse question-answer pairs about that text.
2. Ensure that the questions are relevant to the summary provided and vary in difficulty.
3. Return ONLY valid YAML that follows this exact schema:

questions:
- question: "<string>"
  answer: "<string>"
"""


def generate_questions_yaml(context: str, n_questions: int = 10) -> str:
    """Ask the LLM to create QA pairs in YAML."""
    try:
        response = litellm.completion(
            model=OPENAI_QA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Create {n_questions} questions and answers "
                    f"about:\n\n{context}",
                },
            ],
            temperature=0.3,
            top_p=0.9,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
        )
        return response.choices[0].message.content.strip()
    except Exception as err: # General exception for litellm errors
        logger.error("Q/A generation error: %s", err)
        return ""


def parse_questions_yaml(raw: str) -> list[dict]:
    """
    Convert the LLM output to Python list of dicts.
    Extremely defensive:  1) remove ``` fences  2) try YAML loader
                          3) fallback to regex extraction
    """
    txt = re.sub(r"```[^`]*```", "", raw, flags=re.S).strip()

    # Try normal YAML parsing first
    try:
        data = yaml.safe_load(txt)
        if isinstance(data, dict) and "questions" in data:
            return data["questions"]
    except yaml.YAMLError:
        pass

    # Fallback regex: - question: "...", answer: "..."
    qa_pairs = re.findall(
        r'question:\s*["“](.*?)["”]\s*.*?answer:\s*["“](.*?)["”]', txt, flags=re.S
    )
    return [{"question": q.strip(), "answer": a.strip()} for q, a in qa_pairs]


# ───────────────────────  Dataset builder  ─────────────────────────────────
def build_dataset(
    src_dir: str, include_ext: list[str] | tuple[str]
) -> tuple[list[dict], list[dict]]:
    """
    Walk over src_dir, create corpus & query lists ready to save as jsonl.
    """
    corpus, queries = [], []
    corpus_id = 0
    query_id = 0
    timestamp = datetime.utcnow().isoformat()

    for root, _, files in os.walk(src_dir):
        for fname in files:
            if "_" not in include_ext and not any(
                fname.lower().endswith(ext) for ext in include_ext
            ):
                continue

            path = os.path.join(root, fname)
            text = extract_contents(path)
            if not text:
                continue

            # ---------------- corpus entry ----------------
            cid = str(corpus_id)
            corpus_id += 1
            corpus.append({"_id": cid, "title": fname, "text": text})

            # --------------- questions --------------------
            summary = create_summary(text) or text[:2000]  # fallback to raw text
            qa_yaml = generate_questions_yaml(summary)
            questions = parse_questions_yaml(qa_yaml)

            if not questions:
                logger.error("No Q/A pairs parsed for %s", fname)
                continue

            for qa in questions:
                queries.append(
                    {
                        "_id": str(query_id),
                        "text": qa["question"],
                        "references": [{"corpus_id": cid, "score": 1.0}],
                        "ref_answer": qa["answer"],
                        "metadata": {"source_file": fname, "generated_at": timestamp},
                    }
                )
                query_id += 1

    return corpus, queries


# ─────────────────────────────  Main  ──────────────────────────────────────
# The 'run' function below is removed as its functionality (writing to files)
# will be handled by the generator class, or this script will only be a library.
# def run(source_dir, output_dir, include_ext=".md") -> None:
#     corpus, queries = build_dataset(source_dir, include_ext)
# 
#     with open(os.join(output_dir, "corpus.jsonl"), "w", encoding="utf-8") as f_corp:
#         for doc in corpus:
#             f_corp.write(json.dumps(doc, ensure_ascii=False) + "\n")
# 
#     with open(os.join(output_dir, "queries.jsonl"), "w", encoding="utf-8") as f_que:
#         for q in queries:
#             f_que.write(json.dumps(q, ensure_ascii=False) + "\n")
# 
#     logger.info("Dataset built: %d documents, %d queries", len(corpus), len(queries))
#     return corpus, queries

# Any if __name__ == "__main__": block would also be removed.
