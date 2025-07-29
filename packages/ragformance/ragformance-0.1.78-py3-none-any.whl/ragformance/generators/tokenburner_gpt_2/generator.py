import os
import json 
from pathlib import Path
from typing import List, Tuple, Dict, Any

from ragformance.generators.data_generator_interface import RAGformanceGeneratorInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

from .main import main as run_gpt2_script_logic 
# This assumes main.py will be refactored to have a 'main' function 
# that accepts a dictionary of arguments and saves corpus.jsonl / queries.jsonl.

class TokenBurnerGPT2Generator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and Q&A from PDFs using TokenBurner GPT-2 logic.

        Args:
            config: A dictionary containing configuration parameters:
                - pdf_path (str): Path to the source PDF file.
                - output_path (str): Directory to save generated files.
                - model_path (str, optional): Path to a local GPT-2 model (if applicable).
                - max_pages (int, optional): Max pages to process from PDF.
                - llm_api_key (str): API key for OpenAI (or compatible) API.
                - llm_base_url (str): Base URL for OpenAI (or compatible) API.
                - llm_model_name (str): Model name to use for OpenAI calls (e.g., OCR, Q&A).
        """
        pdf_path_str = config["pdf_path"]
        output_dir_str = config["output_path"]

        Path(output_dir_str).mkdir(parents=True, exist_ok=True)

        # --- Adapting script arguments for the refactored main function ---
        # The refactored main function in main.py will expect a dictionary of arguments.
        script_args = {
            "pdf_path": pdf_path_str,         # Corresponds to how main.py will use it
            "output_dir": output_dir_str,     # Directory where main.py should save its output files
            "model_path": config.get("model_path"), # For local GPT-2 model if used by main.py
            "max_pages": config.get("max_pages"),   # If main.py supports max_pages for PDF processing
            "api_key": config["llm_api_key"],       # For OpenAI calls within main.py
            "base_url": config["llm_base_url"],     # For OpenAI calls
            "model_name": config["llm_model_name"], # For OpenAI calls
            # Add any other parameters that the refactored main.py script might need
        }
        
        # This call assumes run_gpt2_script_logic is refactored to accept
        # a dictionary of arguments, and that it saves 
        # 'corpus.jsonl' and 'queries.jsonl' in the output_dir_str.
        run_gpt2_script_logic(script_args) 

        # After run_gpt2_script_logic completes, load the generated files.
        corpus: List[DocModel] = []
        corpus_file = Path(output_dir_str) / "corpus.jsonl"
        if corpus_file.exists():
            with open(corpus_file, "r", encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    corpus.append(DocModel(**data))
        else:
            print(f"Warning: {corpus_file} not found after TokenBurner GPT-2 execution.")

        queries: List[AnnotatedQueryModel] = []
        queries_file = Path(output_dir_str) / "queries.jsonl"
        if queries_file.exists():
            with open(queries_file, "r", encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    # Handle potential variations in relevant_document_ids key
                    relevant_docs = []
                    if "relevant_doc_id" in data and data["relevant_doc_id"]: # Single ID case
                         relevant_docs = [{"corpus_id": str(data["relevant_doc_id"]), "score": 1.0}]
                    elif "relevant_document_ids" in data: # List of dicts case
                         relevant_docs = data["relevant_document_ids"]
                    
                    queries.append(AnnotatedQueryModel(
                        _id=data.get("_id", f"query_gpt2_{len(queries)}"),
                        query_text=data.get("question", data.get("query_text", "")), # Accept "question" or "query_text"
                        relevant_document_ids=relevant_docs,
                        ref_answer=data.get("answer", data.get("ref_answer", "")), # Accept "answer" or "ref_answer"
                        metadata=data.get("metadata", {})
                    ))
        else:
            print(f"Warning: {queries_file} not found after TokenBurner GPT-2 execution.")
        
        print(f"[TokenBurnerGPT2Generator.run] TokenBurner GPT-2 processing complete. Files in {output_dir_str}")
        return corpus, queries
