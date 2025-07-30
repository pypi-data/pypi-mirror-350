from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class LLMConfigItem(BaseModel):
    name: str
    provider: str
    model: str
    api_key_env: str
    params: Dict[str, Any] = {}

class EmbeddingConfigItem(BaseModel):
    name: str
    provider: str
    model: str
    api_key_env: str
    params: Dict[str, Any] = {}

class QuestionDistributionItem(BaseModel):
    type: str
    ratio: float

class RagasGeneratorConfig(BaseModel):
    data_path: str
    output_path: str
    llm_config: LLMConfigItem
    embedding_config: EmbeddingConfigItem
    critique_llm_config: Optional[LLMConfigItem] = None
    n_questions: int = 10
    save_ragas_kg: bool = True
    question_distribution: Optional[List[QuestionDistributionItem]] = None
