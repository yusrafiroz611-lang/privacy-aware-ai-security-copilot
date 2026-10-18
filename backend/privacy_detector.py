import re

PATTERNS = {
    "AADHAAR": re.compile(
        r"(?i)\b(?:aadhaar|aadhar|uid)"
        r"\s*(?:number|no\.?)?\s*[:#=-]?\s*"
        r"[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}\b"
    ),
    "ACCOUNT_NUMBER": re.compile(
        r"(?i)\b(?:(?:bank\s+)?account"
        r"(?:\s+number|\s+no\.?)?|a/c)"
        r"\s*[:#=-]?\s*[A-Z0-9-]{6,20}\b"
    ),
    "EMAIL": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "PAN": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
    "PHONE": re.compile(
        r"(?<!\w)\+?\d{1,3}[ .-]?"
        r"(?:\(?\d{3}\)?[ .-]?)?\d{3}[ .-]?\d{4}(?!\w)"
    ),
}


def detect_and_mask(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > 20000:
        raise ValueError("Text cannot exceed 20,000 characters.")

    findings = []
    sanitized_text = text

    for entity_type, pattern in PATTERNS.items():
        matches = list(pattern.finditer(sanitized_text))
        for match in reversed(matches):
            findings.append({"type": entity_type})
            sanitized_text = (
                sanitized_text[:match.start()]
                + f"[REDACTED_{entity_type}]"
                + sanitized_text[match.end():]
            )

    return {
        "sanitized_text": sanitized_text,
        "findings": findings,
        "total_detected": len(findings),
    }
