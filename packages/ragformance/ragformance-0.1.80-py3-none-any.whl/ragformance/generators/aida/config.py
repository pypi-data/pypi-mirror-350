from pydantic import BaseModel

class AidaGeneratorConfig(BaseModel):
    seed_questions_path: str
    data_dir: str
    output_dir: str
    llm_api_key: str
    llm_base_url: str
    hf_embed_model: str
    capella_xml_path: str
    entity_model_name: str
    qa_model_name: str
    chunk_size: int = 750
    chunk_overlap: int = 100
    persist_dir: str = "chroma_index"
    k_pdf: int = 5
    k_capella: int = 8
