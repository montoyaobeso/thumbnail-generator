from src.app.constants import ALLOWED_CONTENT_TYPE, ALLOWED_INPUT_FORMATS
from fastapi.exceptions import HTTPException
from fastapi import status


def validate_content_type(filename: str, content_type: str) -> bool:
    if content_type not in ALLOWED_CONTENT_TYPE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Supported formats: {ALLOWED_INPUT_FORMATS}; provided '{filename}'.",
        )
