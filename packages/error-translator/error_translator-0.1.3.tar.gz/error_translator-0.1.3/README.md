# ErrorTranslator

ErrorTranslator is a Python library that translates Python error tracebacks into clear, actionable explanations using AI-powered translation models. It supports multiple backends including OpenAI GPT, HuggingFace models, and local models.

---

## Features

- Translate Python exceptions into easy-to-understand suggestions.
- Supports OpenAI GPT, HuggingFace remote models, and local HuggingFace models.
- Caches translations to avoid repeated API calls.
- Displays nicely formatted error and translation outputs using [Rich](https://github.com/Textualize/rich).
- Supports asynchronous translation.

---

## Installation

```bash
pip install error-translator
```

---

## Requirements

- Python 3.7+
- `rich`
- `python-dotenv`
- Other dependencies depending on model backends (e.g., `openai`, `transformers`)

---

## Usage

```python
import os
from error_translator import ErrorTranslator

# Load your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

translator = ErrorTranslator.with_openai(api_key=api_key)

def buggy_function():
    return 1 / 0

try:
    buggy_function()
except Exception as e:
    translator.translate_error(e)
```

---

## Available Models

- `ErrorTranslator.with_openai(api_key, model="gpt-4o")`  
- `ErrorTranslator.with_huggingface(model_name)`  
- `ErrorTranslator.with_local_huggingface(directory_path)`  
- `ErrorTranslator.with_custom_model(custom_model_instance)`

---

## Environment Variables

Create a `.env` file in your project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Development & Contribution

Feel free to open issues or submit pull requests!

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

Built using [Rich](https://github.com/Textualize/rich) for beautiful console output and various AI translation models.

---

## Example Output

![Error Translator Logs](https://raw.githubusercontent.com/rromikas/error-translator/refs/heads/main/demo.png)
