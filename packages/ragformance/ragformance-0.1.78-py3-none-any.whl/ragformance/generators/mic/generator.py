import os
from pathlib import Path
from typing import List, Tuple, Dict, Any

from ragformance.generators.data_generator_interface import RAGformanceGeneratorInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

# Import the core logic from .main
# The original run function from main.py will be adapted.
from .main import run as run_mic_core_logic 
from .main import DEFAULT_GENERATION_PROMPT # Import default prompt if needed

class MicGenerator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates a corpus and unanswerable questions (Missing Context).

        Args:
            config: A dictionary containing configuration parameters:
                - data_path (str): Path to the source data (manual file, e.g. manual.md).
                - output_path (str): Path to save the generated files (corpus.jsonl, queries.jsonl).
                - llm_model_name (str): Name of the LLM model.
                - llm_prompt_template (str, optional): Custom prompt template. Defaults to DEFAULT_GENERATION_PROMPT.
                - llm_batch_size (int, optional): Batch size for LLM generation. Defaults to 16.
                - num_queries_to_generate (int, optional): Number of queries to generate. Defaults to 20.
        """
        datapath = config["data_path"] # This is the input file path (e.g., manual.md)
        output_path_str = config["output_path"]

        model_name = config["llm_model_name"]
        prompt_template = config.get("llm_prompt_template", DEFAULT_GENERATION_PROMPT)
        batch_size = config.get("llm_batch_size", 16)
        num_queries = config.get("num_queries_to_generate", 20)

        # Ensure output directory exists
        output_dir = Path(output_path_str)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Call the core logic function
        # It returns Tuple[List[Dict], List[Dict]]
        # These are already formatted as dicts ready for DocModel/AnnotatedQueryModel
        raw_queries, raw_corpus = run_mic_core_logic(
            file_path=datapath,
            output_path=output_path_str, # core logic handles saving to this path
            model_name=model_name,
            prompt_template=prompt_template,
            batch_size=batch_size,
            num_queries=num_queries
        )
        
        # Convert raw dicts to Pydantic models
        corpus_models: List[DocModel] = []
        for doc_dict in raw_corpus:
            corpus_models.append(DocModel(**doc_dict))

        queries_models: List[AnnotatedQueryModel] = []
        for query_dict in raw_queries:
            # Ensure relevant_document_ids is a list of dicts or empty list
            relevant_ids = query_dict.get("relevant_document_ids", [])
            if not isinstance(relevant_ids, list): # Basic check, could be more robust
                relevant_ids = []
            
            queries_models.append(AnnotatedQueryModel(
                _id=query_dict["_id"],
                query_text=query_dict["query_text"],
                relevant_document_ids=relevant_ids,
                ref_answer=query_dict.get("ref_answer", "This question can not be answered based on the available data"),
                metadata=query_dict.get("metadata", {})
            ))

        print(f"[MicGenerator.run] MiC generation complete. Files saved in {output_path_str}")
        
        return corpus_models, queries_models
