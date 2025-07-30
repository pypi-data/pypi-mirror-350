from pydantic import BaseModel

class AlphaGeneratorConfig(BaseModel):
    data_path: str
    output_path: str
    temporary_folder: str = "converted_data"
    llm_api_key: str
    llm_base_url: str
    llm_model_name: str
