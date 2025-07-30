from ragformance.generators.base_config import BaseGeneratorConfig

class AlphaGeneratorConfig(BaseGeneratorConfig):
    input_data_path: str  # Overrides base to make it mandatory, formerly data_path
    llm_api_key: str      # Overrides base to make it mandatory
    llm_base_url: str     # Overrides base to make it mandatory
    llm_model_name: str   # Overrides base to make it mandatory
    # output_path is inherited from BaseGeneratorConfig as 'str'

    # Fields specific to AlphaGeneratorConfig
    temporary_folder: str = "converted_data"
