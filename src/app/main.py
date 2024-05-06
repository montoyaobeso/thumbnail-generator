import io
from typing import Annotated

from fastapi import FastAPI, File, Form, Response, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from mangum import Mangum
from PIL import Image


app = FastAPI(
    title="Thumbnail Generator",
    description="Generate a PNG Image thumbnail with FastAPI and Pillow.",
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
    file: UploadFile = File(...),
    width: Annotated[int, Form()] = 128,
    height: Annotated[int, Form()] = 128,
):
    """
    Generate thumbnail images by providing binary data and the desired output size.

    Returns:
        File: IOBytes of the resized image, default format is PNG.
    """
    # Validate input file type
    if file.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Supported formats: [.png, .jpeg, .jpg]; provided '{file.filename}'.",
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
    image.convert("RGB").save(image_buffer, "PNG")
    image_buffer.seek(0)

    # Send image as response
    return StreamingResponse(image_buffer, media_type="image/png")


handler = Mangum(app)
