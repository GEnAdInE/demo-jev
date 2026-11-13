# Demo Jev - MaybeCovered Insurance Claims Desk

Small FastAPI demo showing the Jev API (via `typesafe-sdk`) on an insurance claims scenario: structured answers from text and images, with the raw HTTP exchange shown for each call.

## Features

- Claims desk UI (`static/index.html`), in English and French
- Tsunami / hotline scenarios: batches of claims classified in parallel
- Consistency check across claims
- Primitives: single-answer calls on text or image
- Sushi photo analysis: every `.jpg` / `.jpeg` / `.png` in the project root is listed and analysed (resized to the 280-1568 px range Jev accepts)

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env             # then put your key in TYPESAFE_API_KEY
```

## Run

```bash
uvicorn app:app --reload
```

Open http://127.0.0.1:8000.

## Presentation

See [PRESENTATION.md](PRESENTATION.md) for the Jev vs traditional LLM talk track.

## Files

| File | Role |
|---|---|
| `app.py` | FastAPI routes and Jev client calls |
| `claims.py` | Sample claims and prompts (en/fr) |
| `static/index.html` | Single-page front end |
| `1000033867.jpg`, `1000033869.jpg` | Test photos picked up by the image demo |
| `.env.example` | Template for the API key (never commit `.env`) |
