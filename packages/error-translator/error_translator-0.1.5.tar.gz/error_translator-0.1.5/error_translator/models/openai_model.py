import openai
from .base_model import TranslationModel

class OpenAITranslationModel(TranslationModel):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def translate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior Python developer helping debug code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content or "No response from AI."
        except Exception as e:
            return f"Failed to get AI translation: {str(e)}"