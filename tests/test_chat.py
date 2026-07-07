from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.routers.chat.save_message", new_callable=AsyncMock)
@patch("app.routers.chat.get_chat_reply", new_callable=AsyncMock)
def test_chat_endpoint(mock_get_reply, mock_save_message):
    mock_get_reply.return_value = "mocked reply"
    response = client.post("/chat", json={"text": "hello"})
    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "mocked reply"
    assert "message_id" in body
