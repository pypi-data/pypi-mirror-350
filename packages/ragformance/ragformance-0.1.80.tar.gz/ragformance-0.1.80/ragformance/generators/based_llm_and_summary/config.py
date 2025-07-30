from typing import List, Optional
from pydantic import BaseModel

class BasedLLMSummaryGeneratorConfig(BaseModel):
    data_source_path: str
    output_path: str
    include_extensions: List[str] = [".md"]
    llm_summary_model_name: str
    llm_qa_model_name: str
    llm_api_key: str
    llm_base_url: Optional[str] = None
    use_proxy: bool = False
    proxy_url: Optional[str] = None
    no_proxy_list: Optional[str] = None
    ca_bundle_path: Optional[str] = None
