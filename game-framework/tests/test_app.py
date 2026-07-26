from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_page_contains_game_area():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "game-area" in html
    assert "WASD" in html
