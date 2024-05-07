from unittest import TestCase

from src.app.image_resizer import ImageResizer
from PIL import Image


class TestImageResizer(TestCase):
    def test_resize_image(self):
        # Arrange
        data = Image.open("tests/horse.png")
        image = ImageResizer(
            image=data,
            target_width=128,
            target_height=128,
            output_format="png",
        )
        image.resize()

        # Act
        result = image.get_output_image()

        # Assert
        self.assertTrue(result.size == (128, 128))

    def test_get_original_image_size(self):
        # Arrange
        data = Image.open("tests/horse.png")

        original_image_size = data.size

        image = ImageResizer(
            image=data,
            target_width=128,
            target_height=128,
            output_format="png",
        )

        # Act
        original_size = image.get_original_image_size()

        # Assert
        self.assertTrue(original_size == original_image_size)
