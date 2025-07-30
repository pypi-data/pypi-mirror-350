from typing import List
from pydantic import BaseModel

class TokenBurnerGeneratorConfig(BaseModel):
    pdf_path: str
    categories_file_path: str
    user_queries: List[str]
    output_path: str
    llm_model_name: str
    llm_api_key: str
    llm_base_url: str
