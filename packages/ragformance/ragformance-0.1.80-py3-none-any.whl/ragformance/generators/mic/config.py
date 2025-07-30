from typing import Optional
from pydantic import BaseModel

class MicGeneratorConfig(BaseModel):
    data_path: str
    output_path: str
    llm_model_name: str
    llm_prompt_template: Optional[str] = None
    llm_batch_size: int = 16
    num_queries_to_generate: int = 20
