from fastapi import FastAPI, Response
from mangum import Mangum

app = FastAPI()


@app.get("/")
def get_root():
    print("Hello World!")
    return Response(
        status_code=200,
        content="API Running in Lambda Funcion!",
    )


handler = Mangum(app)
