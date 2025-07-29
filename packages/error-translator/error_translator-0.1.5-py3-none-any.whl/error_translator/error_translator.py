import linecache
import os
import threading
from typing import Dict, Union
import traceback
import hashlib
import pickle
from .models.base_model import TranslationModel
from error_translator.models.huggingface_model import HuggingFaceTranslationModel
from error_translator.models.local_huggingface_model import LocalHuggingFaceTranslationModel
from error_translator.models.openai_model import OpenAITranslationModel
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

class ErrorTranslator:
    def __init__(self, translation_model: TranslationModel):
        self.translation_model = translation_model
        self._cache = {}

    @classmethod
    def with_openai(cls, api_key: str, model: str = "gpt-4o"):
        return cls(OpenAITranslationModel(api_key, model))

    @classmethod
    def with_huggingface(cls, model_name: str):
        return cls(HuggingFaceTranslationModel(model_name))
    
    @classmethod
    def with_local_huggingface(cls, dir: str):
        return cls(LocalHuggingFaceTranslationModel(dir))
    
    @classmethod
    def with_custom_model(cls, model: TranslationModel):
        return cls(model)

    def _get_code_context(self, tb) -> Dict[str, Union[str, None]]:
        frame = tb.tb_frame
        filename = frame.f_code.co_filename
        line_no = tb.tb_lineno
        function = frame.f_code.co_name

        if not os.path.exists(filename):
            return {
                "file": filename,
                "line_number": line_no,
                "function": function,
                "code": "<source unavailable>",
                "full_file": None
            }

        code_context = []
        for i in range(line_no - 5, line_no + 6):
            line = linecache.getline(filename, i).rstrip()
            if line:
                code_context.append(f"{i}: {line}")

        full_file = None
        with open(filename, 'r') as f:
            lines = f.readlines()
            if len(lines) < 200:
                full_file = "".join(lines)

        return {
            "file": filename,
            "line_number": line_no,
            "function": function,
            "code": "\n".join(code_context),
            "full_file": full_file
        }

    def _get_cache_key(self, error: Exception, context: Dict) -> str:
        error_info = {
            'error_type': type(error).__name__,
            'error_msg': str(error),
            'file': context['file'],
            'line': context['line_number'],
            'function': context['function'],
            'code_snippet': context['code']
        }
        
        error_str = pickle.dumps(error_info)
        return hashlib.md5(error_str).hexdigest()

    def _build_prompt(self, error: Exception, context: Dict) -> str:
        error_type = type(error).__name__
        error_msg = str(error)

        prompt = f"""Analyze this error and provide short, clear suggestions for fixing it.

                    Error: {error_type}: {error_msg}
                    File: {context['file']}
                    Function: {context['function']}
                    Line: {context['line_number']}
ß
                    Relevant code:
                    ```python
                    {context['code']}
                    """

        if context['full_file']:
            prompt += f"\nFull file (for context):\n```python\n{context['full_file']}\n```"

        prompt += "\n\nAnalysis:"
        return prompt

    def get_error_translation(self, error: Exception) -> str:
        tb = error.__traceback__
        if not tb:
            return "No traceback available."

        while tb.tb_next:
            tb = tb.tb_next

        context = self._get_code_context(tb)
        cache_key = self._get_cache_key(error, context)

        if cache_key in self._cache:
            return f"(From cache)\n{self._cache[cache_key]}"

        prompt = self._build_prompt(error, context)

        try:
            translation = self.translation_model.translate(prompt)
            self._cache[cache_key] = translation
            return translation
        except Exception as e:
            return f"Failed to get AI translation: {str(e)}"
        
    def translate_error(self, error: Exception) -> None:
        translation = self.get_error_translation(error)
        console = Console(width=100)
        tb = traceback.format_exc()
        console.print(Panel(tb, title="Original Error", border_style="red"))
        console.print(Markdown(translation))
        
    def translate_error_async(self, error: Exception) -> None:
        thread = threading.Thread(target=self.translate_error, args=(error,), daemon=True)
        thread.start()

