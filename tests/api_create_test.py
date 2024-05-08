import io
from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient
from PIL import Image

from src.app.main import app


class UploadTest(TestCase):
    client = TestClient(app)

    def test_upload(self):
        # Arrange
        with open("tests/horse.png", "rb") as f:
            filebody = f.read()

        form_data = {
            "width": 128,
            "height": 128,
            "output_format": "jpeg",
        }

        # Act
        response = self.client.post(
            "/create",
            data=form_data,
            files={
                "file": ("filename.png", filebody),
            },
        )

        # Assert
        ## check status code
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        ## check resulting image size
        image = Image.open(io.BytesIO(response.content))
        self.assertEqual(image.size, (form_data["width"], form_data["height"]))

        ## Check output expected format
        self.assertEqual(response.headers["content-type"], "image/jpeg")
