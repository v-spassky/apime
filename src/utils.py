import sys
from configparser import ConfigParser
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

Provides simple CLI with the following options:
    - python src/utils.py generate-model <output_file_name>
    - python src/utils.py download-random-images <how_much> <target_folder>

    * commands must be ran from the root folder (.../isanime$ <command>)
"""

config = ConfigParser()
config.read('config.ini')


def generate_model(output_name: str) -> None:
    """
    Generates Keras model according to the global variables configurations.
    Saves it to the 'models' folder.
    """

    if K.image_data_format() == 'channels_first':
        input_shape = (
            3,
            config.getint('MODEL_GENERATION', 'IMG_WIDTH'),
            config.getint('MODEL_GENERATION', 'IMG_HEIGHT'),
        )
    else:
        input_shape = (
            config.getint('MODEL_GENERATION', 'IMG_WIDTH'),
            config.getint('MODEL_GENERATION', 'IMG_HEIGHT'),
            3,
        )

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

    model.compile(
        loss='binary_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy'],
    )

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
    )

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        config.get('MODEL_GENERATION', 'TRAIN_DATA_DIR'),
        target_size=(
            config.getint('MODEL_GENERATION', 'IMG_WIDTH'),
            config.getint('MODEL_GENERATION', 'IMG_HEIGHT'),
        ),
        batch_size=config.getint('MODEL_GENERATION', 'BATCH_SIZE'),
        class_mode='binary',
    )

    validation_generator = test_datagen.flow_from_directory(
        config.get('MODEL_GENERATION', 'VALIDATION_DATA_DIR'),
        target_size=(
            config.getint('MODEL_GENERATION', 'IMG_WIDTH'),
            config.getint('MODEL_GENERATION', 'IMG_HEIGHT'),
        ),
        batch_size=config.getint('MODEL_GENERATION', 'BATCH_SIZE'),
        class_mode='binary',
    )

    model.fit_generator(
        train_generator,
        steps_per_epoch=(
            config.getint('MODEL_GENERATION', 'TRAIN_SAMPLES_NMB')
            //
            config.getint('MODEL_GENERATION', 'BATCH_SIZE')
        ),
        epochs=config.getint('MODEL_GENERATION', 'EPOCHS'),
        validation_data=validation_generator,
        validation_steps=(
            config.getint('MODEL_GENERATION', 'VALIDATION_SAMPLES_NMB')
            //
            config.getint('MODEL_GENERATION', 'BATCH_SIZE')
        ),
    )

    model.save(f'models/{output_name}.h5')


def is_anime(image: PIL.Image, model: keras.models.Sequential) -> bool:
    """
    Takes in Keras model and PIL image instance and returns 
    prediction whether the picture is anime.
    """

    img_array = tensorflow.keras.utils.img_to_array(image)
    img_array = tensorflow.expand_dims(img_array, 0)
    img_array = tensorflow.image.per_image_standardization(img_array)

    predictions = model.predict(img_array)
    if config.getboolean('ENVIRONMENT', 'DEBUG'):
        print(f'Predictions vector: {predictions}')

    if predictions[0][0] < config.getfloat('MODEL_GENERATION', 'PREDICTION_THRESH'):
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
                if config.getboolean('ENVIRONMENT', 'DEBUG'):
                    print('saving: ' + file_name)
                f.write(response.content)


if __name__ == '__main__':

    try:
        command = sys.argv[1]

        if command == 'generate-model':
            generate_model(output_name=sys.argv[2])

        elif command == 'download-random-images':
            download_random_images(
                how_much=sys.argv[2],
                folder_path=sys.argv[3],
            )

        else:
            print(f'No such command: {command}.')

    except IndexError:
        print('No command has been provided.')
