from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs_url" in data


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_recommend_reply_valid():
    response = client.post(
        "/recommend-reply",
        json={"student_message": "كيف أقدر أحذف مادة؟", "top_k": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) <= 2


def test_recommend_reply_empty():
    response = client.post(
        "/recommend-reply",
        json={"student_message": "   ", "top_k": 3}
    )
    assert response.status_code == 400