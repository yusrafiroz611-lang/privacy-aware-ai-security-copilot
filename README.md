# Privacy-Aware AI Security Copilot

IBM Z Datathon 2026 project. A dashboard that checks text for sensitive data (email, PAN, Aadhaar, phone, account numbers) before it is shared with AI tools, masks it, and returns an ALLOW / WARN / BLOCK decision.

**Live demo:** https://privacy-copilot-dun.vercel.app

## How it works
`Browser (React dashboard on Vercel)` → `/api/analyze` (Vercel rewrite) → `FastAPI backend on IBM LinuxONE (Ubuntu 24.04, s390x)`

1. User pastes text in the dashboard.
2. The FastAPI backend (`backend/api.py`) detects sensitive patterns with regex rules (`backend/privacy_detector.py`) and masks them, and scores risky access requests with a transparent keyword heuristic (`backend/risk_rules.py`).
3. A second scan of the masked text validates that no supported patterns remain.
4. A `risk_score` (0–1) combines privacy detections and risky-request signals (privilege escalation, destructive actions, bulk export, sensitive targets, policy bypass, external sharing). Score ≥ 0.6 = BLOCK, ≥ 0.3 = WARN, otherwise ALLOW.

## IBM Z / LinuxONE usage
The backend runs as a systemd service on an IBM LinuxONE Community Cloud VM (Ubuntu 24.04, s390x), serving the `/analyze` API on port 8001.

## What is implemented (honest status)
- Rules-based (regex) privacy masking prototype, with a second-pass validation scan
- Keyword/regex risk heuristic for risky access requests (`risk_score`, `risk_signals`)
- ALLOW / WARN / BLOCK decision from the combined rules-based score
- React dashboard showing findings, masked text, decision and audit fields

## Not implemented yet
- No trained ML/insider-threat model: `risk_score` comes from hand-written rules (`rules-heuristic-v1`) and can miss or over-flag requests
- No generative AI explanation (a rule-based text explanation is returned instead)
- `audit_id` is generated per request but not stored in a database
- `experimental/` contains separate modules (Presidio-based masking, dataset evaluation, access control, encryption demos) that are **not integrated** into the live app

## Run locally
Backend:
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn api:app --port 8001
```
Frontend (`frontend/src/api.js` uses `/api`; for local dev point `API_BASE_URL` to `http://localhost:8001` and run):
```bash
cd frontend
npm install
npm run dev
```

## API
`POST /analyze` with `{"text": "..."}` → `risk_score, high_risk, decision, decision_reason, privacy_detections, privacy_findings, sanitized_text, validation_status, audit_id, timestamp, model_version`. Also `GET /health`.

## Team
Add team member names here.
