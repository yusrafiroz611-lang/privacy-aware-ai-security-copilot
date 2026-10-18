"""Example FastAPI endpoints showing validation, RBAC and privacy checks.

Run locally:
    uvicorn secure_api:app --host 127.0.0.1 --port 8000

Demo only: this example accepts an X-User-Role header to illustrate RBAC.
Do NOT use a client-controlled role header for production authentication.
Integrate a real identity provider/JWT validation before deployment.
"""
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from access_control import require_permission
from leakage_prevention import prepare_for_llm, validate_llm_response

app = FastAPI(title="Privacy-Aware AI Security Copilot - Privacy Module")


class ActivityRequest(BaseModel):
    activity_text: str = Field(min_length=1, max_length=5000)


class ResponseValidationRequest(BaseModel):
    response_text: str = Field(min_length=1, max_length=5000)


def check_role(role: str, permission: str) -> None:
    try:
        require_permission(role, permission)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail="Permission denied") from exc


@app.get("/health")
def health():
    return {"status": "ok", "module": "security-privacy"}


@app.post("/privacy/sanitize")
def sanitize_activity(
    request: ActivityRequest,
    x_user_role: str = Header(default="employee"),
):
    check_role(x_user_role, "submit_activity")
    return prepare_for_llm(request.activity_text)


@app.post("/privacy/validate-response")
def validate_response(
    request: ResponseValidationRequest,
    x_user_role: str = Header(default="employee"),
):
    check_role(x_user_role, "view_own_result")
    return validate_llm_response(request.response_text)
