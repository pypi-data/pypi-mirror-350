from typing import Optional
from pydantic import BaseModel

class LLMPromptGeneratorConfig(BaseModel):
    data_path: str
    output_path: str
    llm_api_key: str
    llm_base_url: str
    llm_model_name: str
    query_gen_prompt_template: Optional[str] = None
    answer_gen_prompt_template: Optional[str] = None
    max_questions_per_doc: int = 5
    process_pdfs: bool = True
    process_markdown: bool = True
