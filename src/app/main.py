import io
from typing import Annotated, Literal

from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from mangum import Mangum
from PIL import Image

from src.app.image_resizer import ImageResizer
from src.app.utils import validate_content_type

app = FastAPI(
    title="Thumbnail Generator",
    description="Generate image thumbnails with FastAPI.",
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
    Generate a thumbnail image by providing binary input data and the desired output size.

    Returns:
        File: IOBytes of the resized image, default format is PNG.
    """
    # Validate input file type
    validate_content_type(file.filename, file.content_type)

    # Get image resizer
    image_buffer = ImageResizer(
        image=Image.open(io.BytesIO(await file.read())),
        target_width=width,
        target_height=height,
        output_format=output_format,
    ).get_output_buffer()

    # Send image as response
    return StreamingResponse(image_buffer, media_type=f"image/{output_format.lower()}")


handler = Mangum(app)
