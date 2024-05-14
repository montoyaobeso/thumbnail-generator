from fastapi import FastAPI
from mangum import Mangum

from src.app.routers import root
from src.app.routers import create

app = FastAPI(
    title="Thumbnail Generator",
    description="Generate image thumbnails with FastAPI.",
    version="0.0.1",
    contact={
        "name": "Abraham Montoya",
        "email": "montoyaobeso@gmail.com",
    },
)

app.include_router(root.router)
app.include_router(create.router)

handler = Mangum(app)
