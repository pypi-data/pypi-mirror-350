from typing import List
from pydantic import BaseModel

class ErrorCodeGeneratorConfig(BaseModel):
    data_path: str
    output_path: str
    corpus_id_prefix: str
    document_title: str
    llm_api_key: str
    llm_base_url: str
    llm_model_name: str
    error_keywords: str = "error, information, or alarm codes (e.g., E09)"
    max_token_context: int = 64000
    question_tags: List[str] = []
    question_category: str = "error code"
