"""Transparent keyword/regex risk heuristic (NOT a machine-learning model)."""
import re

_NUM = r"(?:\d{1,3}(?:,\d{3})+|\d{3,})"

RULES = [
    ("privilege escalation", 0.35, re.compile(
        r"(?i)\b(?:admin(?:istrator|istrative)?|root|superuser|elevated|full|sudo)\b[\w\s-]{0,20}?\b(?:privileges?|access|rights|permissions?)\b"
        r"|\bgrant(?:ed|ing)?\s+(?:all|admin)\b|\belevat\w*\s+(?:my\s+)?(?:privileges?|access)\b|\bsudo\b")),
    ("destructive action", 0.40, re.compile(
        r"(?i)\b(?:drop|truncate|wipe|erase|purge)\s+(?:the\s+)?(?:all\s+)?(?:tables?|database|databases|records|logs|backups?)\b"
        r"|\bdelete\s+(?:all|the\s+entire|every)\b|\bdisable\s+(?:the\s+)?(?:audit|logging|logs|antivirus|security|monitoring|mfa|2fa)\b")),
    ("bulk data export", 0.30, re.compile(
        r"(?i)\b(?:export|download|copy|extract|dump|transfer|exfiltrate)\w*\b[^.]{0,60}?(?:\bbulk\b|\bentire\b|\ball\b|\bfull\b|" + _NUM + r")"
        r"|\b(?:bulk|mass)\s+(?:export|download|copy|extract)")),
    ("sensitive data target", 0.25, re.compile(
        r"(?i)\b(?:credit\s*card|card\s+numbers?|customer\s+(?:database|data|records)|client\s+(?:list|emails?|data|records)|production\s+(?:database|db|server)"
        r"|payroll|salary\s+data|passwords?|ssn|social\s+security|medical\s+records|pii|source\s+code|api\s+keys?|secrets?)\b")),
    ("evasion or policy bypass", 0.30, re.compile(
        r"(?i)\b(?:bypass|circumvent|without\s+(?:approval|authori[sz]ation|permission|logging)|avoid\s+detection|hide\s+(?:this|the)\s+(?:activity|access))\b")),
    ("external sharing", 0.30, re.compile(
        r"(?i)\b(?:personal\s+(?:email|gmail|drive|cloud|usb)|external\s+(?:party|email|drive)|usb\s+(?:drive|stick)|public\s+(?:link|repo|paste)|competitor)\b")),
]

MITIGATING = re.compile(r"(?i)\b(?:read[- ]only|view[- ]only|general|public\s+documentation|wiki|troubleshooting)\b")
MITIGATION_WEIGHT = 0.15


def assess_risk(text):
    """Return (score 0..1, list of triggered signal names)."""
    score = 0.0
    signals = []
    for name, weight, pattern in RULES:
        if pattern.search(text):
            score += weight
            signals.append(name)
    if signals and MITIGATING.search(text):
        score -= MITIGATION_WEIGHT
    return round(max(0.0, min(1.0, score)), 2), signals
