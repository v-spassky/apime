from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
)
import requests
import keras
import tensorflow
import src.utils

"""
This module manages handling HTTP requests.
"""

app = FastAPI()
model = keras.models.load_model('models/third_try.h5')


@app.post("/is_it_anime")
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
            detail=f'No picture URL detected in the request`s headres.')

    try:
        image = tensorflow.keras.preprocessing.image.load_img(
            tensorflow.keras.utils.get_file(origin=picture_url),
            target_size=(150, 150))

        if src.utils.is_anime(image, model):
            return 'Yes'
        else:
            return 'No'

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Could not get the image.')
