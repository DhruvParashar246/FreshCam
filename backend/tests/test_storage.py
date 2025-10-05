import os
import json
import pytest

from fastapi.testclient import TestClient

from backend.app import app
from backend.services.gemini_storage import generate_storage_advice

client = TestClient(app)


def test_generate_storage_advice_mock():
    os.environ["GEMINI_API_KEY"] = "mock"
    advice, raw = generate_storage_advice("apple", ripeness="ripe", quantity=3)
    assert "apple" in advice.lower() or isinstance(advice, str)
    parsed = json.loads(raw)
    assert "advice" in parsed


def test_storage_advice_endpoint_mock():
    os.environ["GEMINI_API_KEY"] = "mock"
    payload = {"fruit": "banana", "ripeness": "ripe", "quantity": 2}
    resp = client.post("/storage-advice", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["fruit"] == "banana"
    assert "advice" in data

import os
import json
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)


def test_storage_advice_mock():
    os.environ["GEMINI_API_KEY"] = "mock"
    payload = {"fruit": "apple", "ripeness": "ripe", "quantity": 3}
    resp = client.post("/storage-advice", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["fruit"] == "apple"
    assert "advice" in data and len(data["advice"]) > 0
    # raw should be empty in non-debug mode
    assert data.get("raw") is None

