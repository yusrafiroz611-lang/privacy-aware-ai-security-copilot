"""Pre-LLM and post-LLM checks for possible sensitive-data leakage."""
import re
from typing import Any

from privacy import analyze_sensitive_data, mask_sensitive_data

# Basic demo patterns. These are indicators, not a complete DLP system.
PATTERNS = {
    "email_like": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone_like": re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)"),
    "possible_secret": re.compile(
        r"(?i)\b(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*\S+"
    ),
}


def inspect_text(text: str) -> dict[str, Any]:
    """Return a privacy report. Avoid logging the raw input in production."""
    findings = analyze_sensitive_data(text)
    pattern_hits = [name for name, pattern in PATTERNS.items() if pattern.search(text)]
    return {
        "pii_detected": bool(findings),
        "pii_findings": findings,
        "pattern_alerts": pattern_hits,
        "needs_review": bool(findings or pattern_hits),
    }


def prepare_for_llm(text: str) -> dict[str, Any]:
    """Inspect and mask user input before it is sent to a generative AI model."""
    report = inspect_text(text)
    return {
        "sanitized_text": mask_sensitive_data(text),
        "privacy_report": report,
    }


def validate_llm_response(response_text: str) -> dict[str, Any]:
    """Check model output before showing it to the user."""
    report = inspect_text(response_text)
    return {
        "safe_to_display": not report["needs_review"],
        "response_text": response_text if not report["needs_review"] else
            "[Response withheld: possible sensitive information detected.]",
        "privacy_report": report,
    }
