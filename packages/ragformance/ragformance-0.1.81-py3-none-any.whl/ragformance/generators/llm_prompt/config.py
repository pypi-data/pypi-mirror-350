from typing import Optional # Keep for other fields
from ragformance.generators.base_config import BaseGeneratorConfig

class LLMPromptGeneratorConfig(BaseGeneratorConfig):
    input_data_path: str  # Overrides base to make it mandatory, formerly data_path
    llm_api_key: str      # Overrides base to make it mandatory
    llm_base_url: str     # Overrides base to make it mandatory
    llm_model_name: str   # Overrides base to make it mandatory
    # output_path is inherited (mandatory str)

    # Fields specific to LLMPromptGeneratorConfig
    query_gen_prompt_template: Optional[str] = None
    answer_gen_prompt_template: Optional[str] = None
    max_questions_per_doc: int = 5
    process_pdfs: bool = True
    process_markdown: bool = True
