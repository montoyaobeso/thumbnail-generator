import io
from typing import Annotated, Literal

from fastapi import FastAPI, File, Form, Response, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from mangum import Mangum
from PIL import Image

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
        Form(description="The desired width for the output image. Defaults to 128."),
    ] = 128,
    height: Annotated[
        int,
        Form(description="The desired heigth for the output image. Defaults to 128."),
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
    image = Image.open(io.BytesIO(image_data))

    # Run some resizing checks
    if width <= 0 or height <= 0:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Width and Height values shoulde be greater than 0.",
        )

    # Get input image size
    im_width, im_height = image.size

    # Check new width and heigth
    size_checks = []
    if width > im_width:
        size_checks.append(
            f"Width input value ({width}) is higher than input image width ({im_width})."
        )

    if height > im_height:
        size_checks.append(
            f"Height input value ({height}) is higher than input image width ({im_height})."
        )

    if size_checks:
        return Response(
            content="\n".join(size_checks),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Resize image
    image = image.resize((int(width), int(height)))

    # Save image to buffer
    image_buffer = io.BytesIO()
    image.convert("RGB").save(image_buffer, output_format.upper())
    image_buffer.seek(0)

    # Send image as response
    return StreamingResponse(image_buffer, media_type=f"image/{output_format.lower()}")


handler = Mangum(app)
