# Privacy-Aware AI Copilot

A prototype for detecting and masking potentially sensitive information (PII) in text using Microsoft Presidio and custom recognizers.

## Project structure

```text
privacy-aware-ai-copilot/
├── ai.py
├── requirements.txt
├── .env.example
├── prepare_dataset.py
├── evaluate_dataset.py
├── test_ai.py
└── dataset/
    └── synthetic_pii.jsonl
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your own API key/model if you want the optional AI explanation feature.
4. Make sure `dataset/synthetic_pii.jsonl` is present.

## Run

```bash
python prepare_dataset.py
python evaluate_dataset.py
python -m unittest test_ai.py
python ai.py
```

## Notes

- The custom recognizers detect identifier-like formats; they do not validate official identity records.
- The evaluation metric only checks whether expected values remain in sanitized text. It does not prove all PII was detected or that the system is secure.
- Use synthetic or properly authorized data for testing.
- Keep `.env` and API keys out of version control.

## Interface consistency

The provided `test_ai.py` expects `check_ai_response()` and a string result from `mask_sensitive_data()`, while the supplied `ai.py` currently returns a dictionary and does not define `check_ai_response()`. Align these interfaces before expecting all tests to pass. The evaluation script in this package reads the `sanitized_text` field returned by `ai.py`.
