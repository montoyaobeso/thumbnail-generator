import io

from PIL.PngImagePlugin import PngImageFile


class ImageResizer:
    """Generate the resized image output."""

    def __init__(
        self,
        image: PngImageFile,
        target_width: int,
        target_height: int,
        output_format: str,
    ) -> bytes:
        self.image = image
        self.target_width = target_width
        self.target_height = target_height
        self.image_width = self.image.size[0]
        self.image_height = self.image.size[1]
        self.output_format = output_format
        self.output_image = None

    def get_original_image_size(self):
        """Get the original input image

        Returns:
            tuple: (width, height).
        """
        return self.image_width, self.image_height

    def resize(self):
        """Resize image and store it internally"""
        self.output_image = self.image.resize(
            (
                int(self.target_width),
                int(self.target_height),
            )
        )

    def get_output_image(self):
        """Get the resized image.

        Returns:
            bytes: Resized image.
        """
        if self.output_image is None:
            self.resize()
        return self.output_image

    def get_output_buffer(self):
        """Return a stremeable buffer for response purposes.

        Returns:
            io.Bytes(): Resized image buffer.
        """
        print(self.output_image)
        if self.output_image is None:
            self.resize()
        self.image_buffer = io.BytesIO()
        self.output_image.convert("RGB").save(
            self.image_buffer, self.output_format.upper()
        )
        self.image_buffer.seek(0)
        return self.image_buffer
