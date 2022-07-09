from pyparsing import DebugExceptionAction
import requests
import PIL
import keras
import tensorflow
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K


"""
This module contains all the auxiliary functions that handle 
creation and usage of a Keras model, and configuration thereof.
"""

IMG_WIGTH, IMG_HEIGHT = 150, 150
TRAIN_DATA_DIR = 'data/train'
VALIDATION_DATA_DIR = 'data/validation'
TRAIN_SAMPLES_NMB = 700
VALIDATION_SAMPLES_NMB = 120
EPOCHS = 25
BATCH_SIZE = 16
PREDICTION_THRESH = 1e-16
DEBUG = True


def generate_model() -> None:
    """
    Generates Keras model according to the global variables configurations.
    """

    if K.image_data_format() == 'channels_first':
        input_shape = (3, IMG_WIGTH, IMG_HEIGHT)
    else:
        input_shape = (IMG_WIGTH, IMG_HEIGHT, 3)

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        TRAIN_DATA_DIR,
        target_size=(IMG_WIGTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='binary')

    validation_generator = test_datagen.flow_from_directory(
        VALIDATION_DATA_DIR,
        target_size=(IMG_WIGTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='binary')

    model.fit_generator(
        train_generator,
        steps_per_epoch=TRAIN_SAMPLES_NMB // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=validation_generator,
        validation_steps=VALIDATION_SAMPLES_NMB // BATCH_SIZE)

    model.save('models/keras_model_v4.h5')


def is_anime(image: PIL.Image, model: keras.models.Sequential) -> bool:
    """
    Takes in Keras model and PIL image instance and returns 
    prediction whether the picture is anime.
    """

    img_array = tensorflow.keras.utils.img_to_array(image)
    img_array = tensorflow.expand_dims(img_array, 0)
    img_array = tensorflow.image.per_image_standardization(img_array)

    predictions = model.predict(img_array)
    if DEBUG:
        print(f'Predictions vector: {predictions}')

    if predictions[0][0] < PREDICTION_THRESH:
        is_anime = True
    else:
        is_anime = False

    return is_anime


def download_random_images(how_much: int, folder_path: str) -> None:
    """
    Downloads how_much images into folder_path.
    """

    for i in range(1, how_much+1):

        url = 'https://picsum.photos/150/150/?random'
        response = requests.get(url)

        if response.status_code == 200:

            file_name = f'not_anime_{i}.jpg'
            file_path = f'{folder_path}/{file_name}'

            with open(file_path, 'wb') as f:
                print('saving: ' + file_name)
                f.write(response.content)
