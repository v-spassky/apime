from configparser import ConfigParser
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
)
import keras
import tensorflow
from .utils import is_anime

"""
This module manages handling HTTP requests.

Launched form the root folder like this:
.../isanime$ uvicorn src.server:app
"""

config = ConfigParser()
config.read('config.ini')

keras_model_name = config['SERVER']['MODEL_NAME']
model = keras.models.load_model(f'models/{keras_model_name}.h5')

app = FastAPI()


@app.post('/is_it_anime')
async def is_it_anime(request: Request):
    """
    Handles HTTP post requests to /is_it_anime.
    Must contain picture URL under the pfp-url header.
    Throws error with status code 400 if no URL provided, 
    or if the URL is invalid. Returns string 'Yes' or 'No' as a prediction.
    """

    picture_url = request.headers.get('pfp-url')

    if not picture_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No picture URL detected in the request`s headres.',
        )

    try:
        image = tensorflow.keras.preprocessing.image.load_img(
            tensorflow.keras.utils.get_file(origin=picture_url),
            target_size=(150, 150),
        )

        if is_anime(image, model):
            return {'conclusion': 'Yes'}
        else:
            return {'conclusion': 'No'}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Could not get the image.',
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Sorry! Unknown error occured.',
        )
