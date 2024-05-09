import io

import requests
from PIL import Image

if __name__ == "__main__":
    with open("tests/horse.png", "rb") as f:
        response = requests.post(
            "http://127.0.0.1:80/create",
            data={
                "width": 128,
                "height": 128,
                "output_format": "jpeg",
            },
            files={"file": f.read()},
        )

        print(response.headers)

        image = Image.open(io.BytesIO(response.content))

        image.show()
