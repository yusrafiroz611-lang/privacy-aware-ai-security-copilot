"""PII detection and masking using Microsoft Presidio.

Usage:
    from privacy import mask_sensitive_data, analyze_sensitive_data
    safe_text = mask_sensitive_data("Contact Rahul at rahul@example.com")
"""
from typing import Any, Dict, List

try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
    from presidio_anonymizer.entities import OperatorConfig
except ImportError as exc:
    raise ImportError(
        "Presidio is not installed. Run: pip install -r requirements.txt"
    ) from exc

_analyzer = AnalyzerEngine()
_anonymizer = AnonymizerEngine()

DEFAULT_ENTITIES = [
    "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER",
    "CREDIT_CARD", "IBAN_CODE", "IP_ADDRESS",
]


def analyze_sensitive_data(text: str, language: str = "en") -> List[Dict[str, Any]]:
    """Return detected PII findings without returning the original text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    results = _analyzer.analyze(
        text=text, language=language, entities=DEFAULT_ENTITIES
    )
    return [
        {
            "entity_type": item.entity_type,
            "start": item.start,
            "end": item.end,
            "score": round(float(item.score), 3),
        }
        for item in results
    ]


def mask_sensitive_data(text: str, language: str = "en") -> str:
    """Replace recognized PII with entity labels before sending text to an LLM."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    results = _analyzer.analyze(
        text=text, language=language, entities=DEFAULT_ENTITIES
    )
    operators = {
        entity: OperatorConfig("replace", {"new_value": f"<{entity}>"})
        for entity in DEFAULT_ENTITIES
    }
    return _anonymizer.anonymize(
        text=text, analyzer_results=results, operators=operators
    ).text
