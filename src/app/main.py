import io
from typing import Annotated, Literal

from fastapi import FastAPI, File, Form, Response, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from mangum import Mangum
from PIL import Image

from app.image_resizer import ImageResizer

app = FastAPI(
    title="Thumbnail Generator",
    description="Generate image thumbnail with FastAPI and Pillow.",
    version="0.0.1",
    contact={
        "name": "Abraham Montoya",
        "email": "montoyaobeso@gmail.com",
    },
)


@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Welcome to thumbnail generator API."},
        status_code=status.HTTP_200_OK,
    )


@app.post("/create")
async def get_thumbnail(
    file: UploadFile = File(..., description="Binary image data."),
    width: Annotated[
        int,
        Form(
            description="The desired width for the output image. Defaults to 128.",
            gt=0,
        ),
    ] = 128,
    height: Annotated[
        int,
        Form(
            description="The desired heigth for the output image. Defaults to 128.",
            gt=0,
        ),
    ] = 128,
    output_format: Annotated[
        Literal["png", "jpeg"],
        Form(
            description="Available formats: png and jpeg",
        ),
    ] = "png",
):
    """
    Generate thumbnail images by providing binary data and the desired output size.

    Returns:
        File: IOBytes of the resized image, default format is PNG.
    """
    # Validate input file type
    if file.content_type not in ["image/png", "image/jpeg"]:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Supported formats: [.png, .jpeg]; provided '{file.filename}'.",
        )

    # Read image data
    image_data = await file.read()

    image = ImageResizer(
        image=Image.open(io.BytesIO(image_data)),
        target_width=width,
        target_height=height,
        output_format=output_format,
    )

    # Perfrom resizing
    image.resize()

    # Get output buffer
    image_buffer = image.get_output_buffer()

    # Send image as response
    return StreamingResponse(image_buffer, media_type=f"image/{output_format.lower()}")


handler = Mangum(app)
