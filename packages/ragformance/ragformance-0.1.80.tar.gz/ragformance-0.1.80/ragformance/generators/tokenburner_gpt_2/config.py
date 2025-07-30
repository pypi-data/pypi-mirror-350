from typing import Optional
from pydantic import BaseModel

class TokenBurnerGPT2GeneratorConfig(BaseModel):
    pdf_path: str
    output_path: str
    model_path: Optional[str] = None
    max_pages: Optional[int] = None
    llm_api_key: str
    llm_base_url: str
    llm_model_name: str
