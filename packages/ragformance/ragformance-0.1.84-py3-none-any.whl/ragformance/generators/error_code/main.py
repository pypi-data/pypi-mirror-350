from ragformance.generators.generators.error_code.parsing_engine import (
    find_pages,
    merge_pages,
    extract_keywords,
)
from ragformance.generators.generators.error_code.question_generation import (
    generate_easy_question,
    question_variation,
    add_augmented_question,
)
import numpy as np

# The run function is removed as its logic is now encapsulated in ErrorCodeGenerator.
# Helper functions are imported directly by ErrorCodeGenerator from 
# parsing_engine.py and question_generation.py.
# This file might become empty or be removed if no other shared utilities are placed here.
