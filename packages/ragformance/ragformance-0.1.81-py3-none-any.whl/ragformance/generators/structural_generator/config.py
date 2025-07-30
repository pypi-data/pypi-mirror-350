from pydantic import BaseModel

class StructuralGeneratorConfig(BaseModel):
    data_folder_path: str
    data_file_name: str
    output_path: str
