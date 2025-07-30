from typing import List, Optional
from ragformance.generators.base_config import BaseGeneratorConfig

class BasedLLMSummaryGeneratorConfig(BaseGeneratorConfig):
    input_data_path: str      # Overrides base to make it mandatory, formerly data_source_path
    llm_api_key: str          # Overrides base to make it mandatory
    # output_path is inherited (mandatory str)
    # llm_base_url is inherited (Optional[str])
    # llm_model_name is inherited (Optional[str])

    # Fields specific to BasedLLMSummaryGeneratorConfig
    include_extensions: List[str] = [".md"]
    llm_summary_model_name: str
    llm_qa_model_name: str
    use_proxy: bool = False
    proxy_url: Optional[str] = None
    no_proxy_list: Optional[str] = None
    ca_bundle_path: Optional[str] = None
