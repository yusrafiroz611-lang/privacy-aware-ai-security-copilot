# Security & Privacy Module
For the Privacy-Aware AI Security Copilot — IBM Z Datathon 2026.

## What is included
- `privacy.py`: Microsoft Presidio PII detection and masking.
- `access_control.py`: example role-based permission checks.
- `encryption.py`: Fernet authenticated encryption helpers.
- `leakage_prevention.py`: input sanitization and output inspection.
- `secure_api.py`: example FastAPI endpoints with input validation and RBAC checks.

## Setup
Use Python 3.10–3.12 if available.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

Presidio's English recognizers may need the spaCy model. If installation is constrained, check the Presidio installation guide for a supported model.

## Run the API
```bash
uvicorn secure_api:app --host 127.0.0.1 --port 8000
```
Open `http://127.0.0.1:8000/docs` to try the endpoints.

Example request to `POST /privacy/sanitize`:
```json
{
  "activity_text": "Contact Rahul at rahul@example.com about the account."
}
```
The API returns sanitized text and a privacy report. Send only `sanitized_text` to the LLM.

Example headers:
```text
X-User-Role: employee
```
Supported demo roles: `employee`, `analyst`, `security_admin`.

## Encryption example
```python
from encryption import encrypt_text, decrypt_text

ciphertext, key = encrypt_text("sensitive demo text")
print(decrypt_text(ciphertext, key))
```
For real use, keep keys in a secret manager or protected environment variable. Never store keys beside encrypted data or commit keys to GitHub.

## Important integration notes
1. The RBAC header is only a demo. A real deployment must verify identity with secure authentication (for example, validated JWT/OIDC tokens); never trust a role supplied directly by a client.
2. `validate_llm_response` is a basic safety check, not a guarantee that all sensitive information is detected.
3. Regex and PII recognizers can produce false positives/negatives. Add organization-specific patterns and tests.
4. Do not log raw sensitive prompts or include real company/customer data in tests.
5. Integrate these functions into the main backend. This module does not itself call an LLM, predict insider threats, or connect to PostgreSQL/LinuxONE.
6. Test and run this module in the team's LinuxONE environment before claiming it is deployed there.

## License / open-source references
- Microsoft Presidio: https://github.com/microsoft/presidio
- FastAPI: https://fastapi.tiangolo.com/
- Cryptography (Fernet): https://cryptography.io/
- spaCy: https://spacy.io/
