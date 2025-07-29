from transformers.pipelines import pipeline
from .base_model import TranslationModel

class HuggingFaceTranslationModel(TranslationModel):
    def __init__(self, model: str = "codellama/CodeLlama-7b-hf"):
        self.generator = pipeline("text-generation", model=model)  


    def translate(self, prompt: str) -> str:
        try:
            response = self.generator([{"role": "user", "content": prompt}], do_sample=False, max_new_tokens=1000)
            return response[0]['generated_text'][1]["content"] # type: ignore
        except Exception as e:
            return f"Failed to get HuggingFace translation: {str(e)}"