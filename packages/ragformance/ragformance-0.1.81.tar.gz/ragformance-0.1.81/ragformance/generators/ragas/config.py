from typing import List, Optional, Dict, Any
from pydantic import BaseModel # Keep for nested models
from ragformance.generators.base_config import BaseGeneratorConfig

class LLMConfigItem(BaseModel): # Stays as is
    name: str
    provider: str
    model: str
    api_key_env: str
    params: Dict[str, Any] = {}

class EmbeddingConfigItem(BaseModel): # Stays as is
    name: str
    provider: str
    model: str
    api_key_env: str
    params: Dict[str, Any] = {}

class QuestionDistributionItem(BaseModel): # Stays as is
    type: str
    ratio: float

class RagasGeneratorConfig(BaseGeneratorConfig): # Inherits from BaseGeneratorConfig
    input_data_path: str  # Overrides base to make it mandatory, formerly data_path
    # output_path is inherited (mandatory str)
    # llm_api_key, llm_base_url, llm_model_name are inherited (Optional[str]) and can be ignored

    # Fields specific to RagasGeneratorConfig
    llm_config: LLMConfigItem
    embedding_config: EmbeddingConfigItem
    critique_llm_config: Optional[LLMConfigItem] = None
    n_questions: int = 10
    save_ragas_kg: bool = True
    question_distribution: Optional[List[QuestionDistributionItem]] = None
