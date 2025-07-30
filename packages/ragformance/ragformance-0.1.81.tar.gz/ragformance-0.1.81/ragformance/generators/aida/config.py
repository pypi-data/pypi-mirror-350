from ragformance.generators.base_config import BaseGeneratorConfig

class AidaGeneratorConfig(BaseGeneratorConfig):
    input_data_path: str # Overrides base to make it mandatory, formerly seed_questions_path
    llm_api_key: str     # Overrides base to make it mandatory
    llm_base_url: str    # Overrides base to make it mandatory
    # output_path is inherited from BaseGeneratorConfig as 'str'
    # llm_model_name is inherited from BaseGeneratorConfig as 'Optional[str]'

    # Fields specific to AidaGeneratorConfig
    data_dir: str
    hf_embed_model: str
    capella_xml_path: str
    entity_model_name: str
    qa_model_name: str
    chunk_size: int = 750
    chunk_overlap: int = 100
    persist_dir: str = "chroma_index"
    k_pdf: int = 5
    k_capella: int = 8
