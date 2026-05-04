# Invoice Processor — Capstone Project

An AI agent that extracts and validates invoice data from PDFs, built with the
**Microsoft Agent Framework** and **Azure OpenAI** (Azure AI Foundry).

## Architecture

```
Request
   │
   ▼
┌────────────┐    ┌──────────────────┐    ┌─────────────┐
│ extract_pdf│──▶ │ extract_fields   │──▶ │  validate   │──▶ Response
│  (pypdf)   │    │  (ChatAgent)     │    │ (ChatAgent) │
└────────────┘    └──────────────────┘    └─────────────┘
```

A shared `AgentState` flows through each step.

## Tech Stack

- Microsoft Agent Framework (`agent-framework`) — `ChatAgent` for LLM steps
- Azure OpenAI (Azure AI Foundry) — `AzureOpenAIChatClient`
- FastAPI + Pydantic v2
- pypdf for PDF text extraction
- pytest for tests

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env  # then edit with your values
uvicorn app.main:app --reload
```

### Required environment variables

See `.env.example`. The endpoint must be the **base** URL
(`https://<resource>.cognitiveservices.azure.com/`) — not the chat-completions URL.

## API

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/process_invoice` | POST | Process a single invoice |
| `/api/evaluate` | POST | Run evaluation over a dataset |
| `/health` | GET | Liveness check |

## Evaluation

- **Deterministic:** field-by-field comparison; numeric tolerance 1%; line items
  compared by description (case-insensitive) and numeric tolerance.
- **LLM-as-Judge:** a second `ChatAgent` returns a `0..1` quality score with rationale.

The summary reports per-case scores plus averages.

## Tests

```powershell
pytest
```

## Project Layout

```
app/
  api/         FastAPI routers
  agents/      ChatAgent factories (extractor, validator, judge)
  evaluation/  deterministic + judge + runner
  llm/         Azure OpenAI client + prompts
  schemas/     Pydantic models
  workflow/    Pipeline state and graph
data/          Sample invoices + test cases
tests/         Unit tests
```
