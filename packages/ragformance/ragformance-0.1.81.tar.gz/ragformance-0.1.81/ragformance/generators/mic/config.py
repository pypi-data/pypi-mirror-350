from typing import Optional # Keep for llm_prompt_template
from ragformance.generators.base_config import BaseGeneratorConfig

class MicGeneratorConfig(BaseGeneratorConfig):
    input_data_path: str  # Overrides base to make it mandatory, formerly data_path
    llm_model_name: str   # Overrides base to make it mandatory
    # output_path is inherited (mandatory str)
    # llm_api_key is inherited (Optional[str])
    # llm_base_url is inherited (Optional[str])

    # Fields specific to MicGeneratorConfig
    llm_prompt_template: Optional[str] = None
    llm_batch_size: int = 16
    num_queries_to_generate: int = 20
