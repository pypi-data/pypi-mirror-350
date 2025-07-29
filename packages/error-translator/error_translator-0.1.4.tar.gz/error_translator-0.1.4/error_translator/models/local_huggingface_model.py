from transformers.pipelines import pipeline
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.models.auto.modeling_auto import AutoModelForCausalLM
from .base_model import TranslationModel

class LocalHuggingFaceTranslationModel(TranslationModel):
    def __init__(self, dir: str):
        tokenizer = AutoTokenizer.from_pretrained(dir)
        model = AutoModelForCausalLM.from_pretrained(dir)
        self.generator = pipeline("text-generation", model=model,tokenizer=tokenizer)  


    def translate(self, prompt: str) -> str:
        try:
            response = self.generator([{"role": "user", "content": prompt}], do_sample=False, max_new_tokens=1000)
            return response[0]['generated_text'][1]["content"] # type: ignore
        except Exception as e:
            return f"Failed to get HuggingFace translation: {str(e)}"