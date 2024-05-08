from unittest import TestCase

from fastapi.testclient import TestClient

from src.app.main import app


class TestRootEntrypoint(TestCase):
    client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to thumbnail generator API."}
