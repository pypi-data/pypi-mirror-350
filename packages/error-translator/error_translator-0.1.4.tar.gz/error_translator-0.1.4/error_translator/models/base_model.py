
from abc import ABC, abstractmethod

class TranslationModel(ABC):
    @abstractmethod
    def translate(self, prompt: str) -> str:
        """Translate an error prompt into human-readable explanation"""
        pass