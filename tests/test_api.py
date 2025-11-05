"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAPI:
    """Test cases for API endpoints."""

    def test_root_endpoint(self) -> None:
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self) -> None:
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_evaluate_hand_royal_flush(self) -> None:
        """Test hand evaluation with royal flush."""
        request_data = {
            "cards": [
                {"rank": "A", "suit": "spades"},
                {"rank": "K", "suit": "spades"},
                {"rank": "Q", "suit": "spades"},
                {"rank": "J", "suit": "spades"},
                {"rank": "10", "suit": "spades"},
            ]
        }
        response = client.post("/evaluate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["rank"] == "royal_flush"
        assert "Royal Flush" in data["description"]

    def test_evaluate_hand_pair(self) -> None:
        """Test hand evaluation with pair."""
        request_data = {
            "cards": [
                {"rank": "A", "suit": "hearts"},
                {"rank": "A", "suit": "diamonds"},
                {"rank": "K", "suit": "clubs"},
                {"rank": "Q", "suit": "spades"},
                {"rank": "J", "suit": "hearts"},
            ]
        }
        response = client.post("/evaluate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["rank"] == "pair"
        assert "Pair" in data["description"]

    def test_evaluate_hand_invalid_cards(self) -> None:
        """Test hand evaluation with invalid number of cards."""
        request_data = {
            "cards": [
                {"rank": "A", "suit": "hearts"},
                {"rank": "K", "suit": "diamonds"},
            ]
        }
        response = client.post("/evaluate", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_sample_csv_download(self) -> None:
        """Test sample CSV download."""
        response = client.get("/csv/sample")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert b"player_name" in response.content
        assert b"card1_rank" in response.content
