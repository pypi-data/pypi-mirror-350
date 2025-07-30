from typing import Optional
from pydantic import BaseModel

class BaseGeneratorConfig(BaseModel):
    output_path: str
    input_data_path: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    llm_model_name: Optional[str] = None

    class Config:
        # This allows specific configurations to have extra fields
        # not defined in the base model, which is useful during transition
        # and for fields that are truly unique to a specific generator.
        extra = "allow"
