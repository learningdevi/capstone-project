import os

# Provide dummy env so Settings can load even without a real .env at test time
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://example.cognitiveservices.azure.com/")
os.environ.setdefault("AZURE_OPENAI_KEY", "dummy")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def test_health():
    with TestClient(app) as c:
        r = c.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
