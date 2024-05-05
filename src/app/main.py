from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from mangum import Mangum

app = FastAPI()


@app.get("/")
def get_root():
    print("Hello World!")
    return JSONResponse(
        {
            "message": "API Running in Lambda Funcion!",
        },
        status_code=status.HTTP_200_OK,
    )


handler = Mangum(app)
