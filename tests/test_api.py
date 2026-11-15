from pathlib import Path

from fastapi.testclient import TestClient

from excel_stand.api import app

CORPUS = Path(__file__).parent / "corpus" / "pass"
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_check_rejects_bad_extension():
    r = client.post("/check", files={"file": ("note.txt", b"hello", "text/plain")})
    assert r.status_code == 400
