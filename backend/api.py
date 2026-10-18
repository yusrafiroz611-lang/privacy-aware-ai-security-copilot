
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import os
from fastapi.staticfiles import StaticFiles
from privacy_detector import detect_and_mask
from risk_rules import assess_risk

app = FastAPI(title="Privacy-Aware AI Security Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)


@app.get("/")
def root():
    return {
        "project": "Privacy-Aware AI Security Copilot",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    # Pass 1: detect and mask supported sensitive-data patterns.
    result = detect_and_mask(request.text)
    sanitized_text = result["sanitized_text"]
    count = result["total_detected"]

    # Pass 2: scan the sanitized text for residual supported patterns.
    validation_scan = detect_and_mask(sanitized_text)
    residual_count = validation_scan["total_detected"]

    if residual_count == 0:
        validation_status = "PASSED"
        validation_reason = (
            "No residual patterns from the supported regex checks "
            "were detected in the sanitized text. This is not a "
            "guarantee that all sensitive data has been removed."
        )
    else:
        validation_status = "NEEDS_REVIEW"
        validation_reason = (
            "The second regex scan detected potential residual "
            "sensitive-data patterns. Review is required."
        )

    # Rules-based risk scoring (keyword heuristic + privacy detections); not an ML model.
    privacy_level = 2 if count >= 3 else (1 if count > 0 else 0)
    privacy_floor = {0: 0.0, 1: 0.35, 2: 0.8}[privacy_level]
    heuristic_score, risk_signals = assess_risk(request.text)
    risk_score = round(max(heuristic_score, privacy_floor), 2)

    if risk_score >= 0.6:
        decision = "BLOCK"
    elif risk_score >= 0.3:
        decision = "WARN"
    else:
        decision = "ALLOW"

    parts = []
    if count:
        parts.append(f"{count} sensitive-data pattern(s) detected and masked")
    if risk_signals:
        parts.append("risky-request signals: " + ", ".join(risk_signals))
    if parts:
        reason = "; ".join(parts).capitalize() + "."
    else:
        reason = "No supported sensitive-data patterns or risky-request signals were detected."

    privacy_findings = sorted({
        finding["type"] for finding in result["findings"]
    })

    return {
        "risk_score": risk_score,
        "high_risk": decision == "BLOCK",
        "decision": decision,
        "decision_reason": reason,
        "recommendation": decision,
        "privacy_detections": count,
        "privacy_findings": privacy_findings,
        "sanitized_text": sanitized_text,
        "model_version": "rules-heuristic-v1",
        "risk_signals": risk_signals,
        "genai_explanation": (
            "Rule-based explanation (no generative AI is used): " + reason
        ),
        "validation_status": validation_status,
        "validation_reason": validation_reason,
        "residual_pattern_count": residual_count,
        "audit_id": f"AUD-{uuid4().hex[:12].upper()}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


FRONTEND_DIR = "/home/linux1/privacy_ai_copilot/frontend"
if os.path.isdir(FRONTEND_DIR):
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
