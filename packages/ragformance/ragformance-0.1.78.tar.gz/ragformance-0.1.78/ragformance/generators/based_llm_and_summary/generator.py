import os
import json
from typing import List, Tuple, Dict, Any

from ragformance.generators.data_generator_interface import RAGformanceGeneratorInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

# Assuming helper functions will be imported from the original script,
# which we might rename to e.g., 'core_logic.py' or 'helpers.py'
# For now, let's assume it's 'buildSyntheticDataset_helpers'
from .buildSyntheticDataset import (
    build_dataset, # The main data generation orchestrator
    set_proxy_environment, # Make this callable if generator needs to control it
    # extract_contents, # Used by build_dataset
    # create_summary, # Used by build_dataset
    # generate_questions_yaml, # Used by build_dataset
    # parse_questions_yaml, # Used by build_dataset
)
# Environment variables for LLM config are set in the original script.
# This needs to be handled via the 'config' dict now.

class BasedLLMSummaryGenerator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and queries using the 'based_llm_and_summary' method.

        Args:
            config: A dictionary containing configuration parameters:
                - data_source_path (str): Directory containing source documents.
                - output_path (str): Directory to save generated files (corpus.jsonl, queries.jsonl).
                - include_extensions (list[str], optional): List of file extensions to include. Defaults to [".md"].
                - llm_summary_model_name (str): Name of the LLM for summarization.
                - llm_qa_model_name (str): Name of the LLM for QA generation.
                - llm_api_key (str): API key for the LLM.
                - llm_base_url (str, optional): Base URL for the LLM API.
                - use_proxy (bool, optional): Whether to set proxy env vars. Defaults to False.
                - proxy_url (str, optional): Proxy URL if use_proxy is True.
                - no_proxy_list (str, optional): Comma-separated no_proxy list.
                - ca_bundle_path (str, optional): Path to CA bundle file.
        """
        source_dir = config["data_source_path"]
        output_dir = config["output_path"]
        include_ext = config.get("include_extensions", [".md"]) # Original script had default ".md" in its main.

        # LLM Configuration - to be set as environment variables for litellm if that's how build_dataset expects them.
        # The original script uses os.getenv. We need to ensure these are set if build_dataset relies on them.
        
        # Preserve original env vars to restore them later
        original_env = {}
        keys_to_set = [
            "OPENAI_SUMMARY_MODEL", "OPENAI_QA_MODEL", "OPENAI_API_KEY", 
            "OPENAI_BASE_URL", "PROXY", "NO_PROXY", "CA_BUNDLE",
            "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
            "CURL_CA_BUNDLE", "REQUESTS_CA_BUNDLE", "SSL_CERT_FILE"
        ]
        for key in keys_to_set:
            original_env[key] = os.environ.get(key)

        os.environ["OPENAI_SUMMARY_MODEL"] = config["llm_summary_model_name"]
        os.environ["OPENAI_QA_MODEL"] = config["llm_qa_model_name"]
        os.environ["OPENAI_API_KEY"] = config["llm_api_key"]
        if "llm_base_url" in config and config["llm_base_url"]: # Ensure not empty
            os.environ["OPENAI_BASE_URL"] = config["llm_base_url"]
        else: # Unset if not provided or empty, to avoid litellm using a bad default
            if "OPENAI_BASE_URL" in os.environ: del os.environ["OPENAI_BASE_URL"]
        
        if config.get("use_proxy", False):
            # Populate env vars that set_proxy_environment expects
            if "proxy_url" in config: os.environ["PROXY"] = config["proxy_url"]
            if "no_proxy_list" in config: os.environ["NO_PROXY"] = config["no_proxy_list"]
            if "ca_bundle_path" in config: os.environ["CA_BUNDLE"] = config["ca_bundle_path"]
            set_proxy_environment() # Call the function from buildSyntheticDataset
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # build_dataset returns two lists of dicts, already in the desired format for jsonl
        raw_corpus, raw_queries = build_dataset(source_dir, include_ext)

        # Restore original environment variables
        for key, value in original_env.items():
            if value is None:
                if key in os.environ: del os.environ[key]
            else:
                os.environ[key] = value

        # Convert raw dicts to Pydantic models
        corpus_models: List[DocModel] = []
        for doc_dict in raw_corpus:
            corpus_models.append(DocModel(**doc_dict))

        queries_models: List[AnnotatedQueryModel] = []
        for query_dict in raw_queries:
            metadata = query_dict.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {"original_metadata": metadata}

            queries_models.append(AnnotatedQueryModel(
                _id=query_dict["_id"],
                query_text=query_dict["text"], 
                relevant_document_ids=query_dict.get("references", []),
                ref_answer=query_dict.get("ref_answer", ""),
                metadata=metadata
            ))

        # Write to files (as the original script did, and good for persistence)
        corpus_jsonl_path = os.path.join(output_dir, "corpus.jsonl")
        with open(corpus_jsonl_path, "w", encoding="utf-8") as f_corp:
            for doc_model in corpus_models:
                f_corp.write(doc_model.model_dump_json() + "\n")

        queries_jsonl_path = os.path.join(output_dir, "queries.jsonl")
        with open(queries_jsonl_path, "w", encoding="utf-8") as f_que:
            for query_model in queries_models:
                f_que.write(query_model.model_dump_json() + "\n")
        
        print(f"[BasedLLMSummaryGenerator.run] Dataset built: {len(corpus_models)} documents, {len(queries_models)} queries")
        
        return corpus_models, queries_models
