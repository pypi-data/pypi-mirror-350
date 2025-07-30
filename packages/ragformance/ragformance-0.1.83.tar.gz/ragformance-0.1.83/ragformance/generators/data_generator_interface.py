from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional

# Attempt to import DocModel and AnnotatedQueryModel from their typical locations
# Adjust these imports if the actual location is different
try:
    from ragformance.models.corpus import DocModel
    from ragformance.models.answer import AnnotatedQueryModel
except ImportError:
    # Provide dummy implementations or raise an error if these models are critical
    # and their absence means the interface cannot be meaningfully defined.
    # This is a placeholder for handling the case where models are not found.
    # For now, we'll define them as simple types to allow the interface to be defined.
    # In a real scenario, you'd ensure these are correctly importable or handle their absence.
    DocModel = type("DocModel", (), {}) 
    AnnotatedQueryModel = type("AnnotatedQueryModel", (), {})
    print("Warning: DocModel or AnnotatedQueryModel not found. Using placeholder types.")


class RAGformanceGeneratorInterface(ABC):
    """
    Interface for RAGformance data generators.

    Each generator should implement the `run` method, which takes a configuration
    dictionary and returns a tuple containing a list of document models and a
    list of annotated query models.
    """

    @abstractmethod
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Runs the data generation process.

        Args:
            config: A dictionary containing all necessary configuration parameters
                    for the generator. This can include paths, API keys, model names,
                    generation options, etc.

        Returns:
            A tuple containing two lists:
            1. List[DocModel]: The generated corpus (list of document models).
            2. List[AnnotatedQueryModel]: The generated queries/questions (list of
                                          annotated query models), potentially with
                                          reference answers.
        """
        raise NotImplementedError
