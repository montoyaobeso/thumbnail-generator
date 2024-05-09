from unittest import TestCase
from src.app.utils import validate_content_type
from fastapi.exceptions import HTTPException


class TestValidateContentType(TestCase):
    def test_validate_content_type_as_valid(self):
        # Arrange
        content_type = "image/png"

        # Act
        result = validate_content_type("fake.file", content_type)

        # Assert
        self.assertIsNone(result)

    def test_validate_content_type_as_invalid(self):
        # Arrange
        content_type = "image/invalid"

        # Act
        with self.assertRaises(Exception) as context:
            validate_content_type("fake.file", content_type)

        # Assert
        self.assertIsInstance(context.exception, HTTPException)
