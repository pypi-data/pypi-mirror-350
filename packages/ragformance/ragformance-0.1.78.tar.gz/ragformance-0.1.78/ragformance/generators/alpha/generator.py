import os
import pandas as pd # Keep this if parquet_to_jsonl or other direct uses remain
import json # Keep this if parquet_to_jsonl or other direct uses remain
from typing import List, Tuple, Dict 

# Interface and Models
from ragformance.generators.data_generator_interface import RAGformanceGeneratorInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel
from pydantic import TypeAdapter # If parquet_to_jsonl uses it

# Functions from the old main.py
# Assuming these functions will be part of the class or called by it.
# They might need to be refactored to be methods or static methods.
from .main import ( # Or directly include their code if main.py is removed
    convert_folders_to_markdown,
    summarize,
    _split_into_sentences,
    _chunk_document_fast,
    generate_questions, # This function itself might need heavy refactoring
    parquet_to_jsonl,
    # call_backend_agent, # This is used by summarize and generate_questions
    # parse_qa_pairs_from_response, # Used by generate_questions
    # _extract_tag_content # Used by summarize
)

class AlphaGenerator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and queries using the Alpha generation method.

        Args:
            config: A dictionary containing configuration parameters:
                - data_path (str): Path to the folder containing the data.
                - output_path (str): Path to save the generated files.
                - temporary_folder (str, optional): Path for temporary files. Defaults to "converted_data".
                - llm_api_key (str): API key for the LLM.
                - llm_base_url (str): Base URL for the LLM API.
                - llm_model_name (str): Name of the LLM model.
        """
        folder_path = config["data_path"]
        output_path = config["output_path"]
        temporary_folder = config.get("temporary_folder", "converted_data")
        api_key = config["llm_api_key"]
        api_base_url = config["llm_base_url"]
        api_model = config["llm_model_name"]

        # Ensure output and temporary folders exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if not os.path.exists(temporary_folder):
            os.makedirs(temporary_folder)

        # Convert the folders to markdown files
        # Assuming convert_folders_to_markdown is correctly imported or defined
        convert_folders_to_markdown("", folder_path, temporary_folder)

        for file_name in os.listdir(temporary_folder):
            if not file_name.endswith(".md"):
                continue
            
            file_path = os.path.join(temporary_folder, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f"Reading file {file_name}")
                document = f.read()

                # Assuming summarize is correctly imported or defined
                doc_summary = summarize(document, api_key, api_base_url, api_model)
                
                sentences = _split_into_sentences(document)
                
                # Using file_name without .md as doc_id
                doc_id = file_name.replace(".md", "")
                chunks = _chunk_document_fast(sentences, 512, doc_id) # Max tokens is hardcoded, consider making it configurable

                print(f"Generating questions for {file_name}")
                # Assuming generate_questions is correctly imported or defined
                # generate_questions writes parquet files to output_path
                generate_questions(
                    chunks, 
                    file_name, # Pass file_name (e.g. "doc.md")
                    doc_summary, 
                    output_path, # output_path for parquet files
                    api_key, 
                    api_base_url, 
                    api_model
                )
        
        # Clean up the temporary folder (optional, consider making it configurable)
        # For example, shutil.rmtree(temporary_folder) if you import shutil

        # Convert generated parquet files to JSONL and return
        # Assuming parquet_to_jsonl is correctly imported or defined
        corpus, queries = parquet_to_jsonl(output_path) # parquet_to_jsonl reads from output_path
        
        return corpus, queries
