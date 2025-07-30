from typing import List # Retain List from typing
from ragformance.generators.base_config import BaseGeneratorConfig

class ErrorCodeGeneratorConfig(BaseGeneratorConfig):
    input_data_path: str  # Overrides base to make it mandatory, formerly data_path
    llm_api_key: str      # Overrides base to make it mandatory
    llm_base_url: str     # Overrides base to make it mandatory
    llm_model_name: str   # Overrides base to make it mandatory
    # output_path is inherited (mandatory str)

    # Fields specific to ErrorCodeGeneratorConfig
    corpus_id_prefix: str
    document_title: str
    error_keywords: str = "error, information, or alarm codes (e.g., E09)"
    max_token_context: int = 64000
    question_tags: List[str] = []
    question_category: str = "error code"
