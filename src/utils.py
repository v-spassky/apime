import sys
import os
import glob
import statistics
from configparser import ConfigParser
import concurrent.futures
import requests
import PIL
import keras
import tensorflow
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from .samples import REGULAR_PFP_URLS, ANIME_PFP_URLS


"""
This module contains all the auxiliary functions that handle 
creation and usage of a Keras model, and configuration thereof.

Provides simple CLI with the following options:
    - python src/utils.py generate-model <output_file_name>
    - python src/utils.py download-random-images <how_much> <target_folder> <initial_image_index>
    - python src/utils.py get-model-statistics

    * commands must be ran from the root folder (.../apime$ <command>)
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

    print('Classes and their indices:')
    print(f'Training dataset: {train_generator.class_indices}')
    print(f'Validation dataset: {validation_generator.class_indices}')

    model.fit(
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
    img_array /= 255

    predictions = model.predict(img_array)
    if config.getboolean('ENVIRONMENT', 'DEBUG'):
        print(f'Prediction value: {predictions[0][0]}')

    if predictions[0][0] < config.getfloat('MODEL_GENERATION', 'PREDICTION_THRESH'):
        is_anime = True
    else:
        is_anime = False

    return is_anime


def get_prediction_value(image: PIL.Image, model: keras.models.Sequential) -> bool:
    """
    Returns model predicition value for a given picture.
    """

    img_array = tensorflow.keras.utils.img_to_array(image)
    img_array = tensorflow.expand_dims(img_array, 0)
    img_array /= 255

    prediction = model.predict(img_array)[0][0]
    if config.getboolean('ENVIRONMENT', 'DEBUG'):
        print(f'Prediction value: {prediction}')

    return prediction


def get_model_statistics():
    """
    Runs through pre-defined set of URLs 
    and prints predictions values for them.
    """

    keras_model_name = config.get('SERVER', 'MODEL_NAME')
    model = keras.models.load_model(f'models/{keras_model_name}.h5')

    regular_pfp_scores = []
    anime_pfp_scores = []

    print('Checking regular profile pictures...')

    for url in REGULAR_PFP_URLS:
        img = tensorflow.keras.preprocessing.image.load_img(
            tensorflow.keras.utils.get_file(origin=url),
            target_size=(
                config.getint('MODEL_GENERATION', 'IMG_WIDTH'),
                config.getint('MODEL_GENERATION', 'IMG_HEIGHT'),
            ),
        )
        prediction_value = get_prediction_value(img, model)
        print(f'Got {prediction_value} prediction value for {url}')
        regular_pfp_scores.append(prediction_value)

    print('Checking anime profile pictures...')

    for url in ANIME_PFP_URLS:
        img = tensorflow.keras.preprocessing.image.load_img(
            tensorflow.keras.utils.get_file(origin=url),
            target_size=(
                config.getint('MODEL_GENERATION', 'IMG_WIDTH'),
                config.getint('MODEL_GENERATION', 'IMG_HEIGHT'),
            ),
        )
        prediction_value = get_prediction_value(img, model)
        print(f'Got {prediction_value} prediction value for {url}')
        anime_pfp_scores.append(prediction_value)

    print(f'Scores for regular profile pictures: {regular_pfp_scores}')
    print(f'Scores for anime profile pictures: {anime_pfp_scores}')

    regular_pfp_avg = sum(regular_pfp_scores) / len(regular_pfp_scores)
    anime_pfp_avg = sum(anime_pfp_scores) / len(anime_pfp_scores)

    print(f'Average score for regular profile pictures: {regular_pfp_avg}')
    print(f'Average score for anime profile pictures: {anime_pfp_avg}')

    regular_pfp_median = statistics.median(regular_pfp_scores)
    anime_pfp_median = statistics.median(anime_pfp_scores)

    print(f'Median score for regular profile pictures: {regular_pfp_median}')
    print(f'Median score for anime profile pictures: {anime_pfp_median}')


def download_random_images(
    how_much: int,
    folder_path: str,
    initial_index: int,
) -> None:
    """
    Downloads how_much images into folder_path.
    """

    image_names = [
        f'not_anime_{i}.jpg' for i in range(initial_index, how_much+initial_index)
    ]

    def download_image(file_name) -> None:
        """
        ...
        """

        w = config.getint('MODEL_GENERATION', 'IMG_WIDTH')
        h = config.getint('MODEL_GENERATION', 'IMG_HEIGHT')

        url = f'https://picsum.photos/{w}/{h}/?random'
        response = requests.get(url)

        if response.status_code == 200:

            file_path = f'{folder_path}/{file_name}'

            with open(file_path, 'wb') as f:
                print(f'Saving {file_name} ...')
                f.write(response.content)

    with concurrent.futures.ThreadPoolExecutor(how_much // 100 + 1) as executor:
        executor.map(download_image, image_names)


def filler_unsuitable_images(dirpath: str, remove=False) -> None:
    """
    ...
    """

    if remove:
        print(f'Going to remove unsuitable images in the {dirpath} folder...')
    else:
        print(f'Going to list unsuitable images in the {dirpath} folder...')

    def filter_single_image(path):
        """
        ...
        """

        with PIL.Image.open(path) as img:
            w, h = img.size
            ar = w / h

            if w < 200 or h < 200 or 0.33 > ar > 3:
                print(
                    f'Image {path} has {w=}, {h=}, {ar=} and is for removal.'
                )
                if remove:
                    os.remove(path)
                    print(f'{path} removed.')

    image_paths = glob.glob(f'{dirpath}/*.jpg')
    image_paths.extend(glob.glob(f'{dirpath}/*.jpeg'))
    image_paths.extend(glob.glob(f'{dirpath}/*.png'))
    print('Found such image paths:')
    print(*image_paths[:5], sep='\n')
    print('...')
    print(*image_paths[len(image_paths)-5:], sep='\n')
    print(f'Total: {len(image_paths)}')

    with concurrent.futures.ThreadPoolExecutor(len(image_paths) // 100 + 1) as executor:
        executor.map(filter_single_image, image_paths)


if __name__ == '__main__':

    try:
        command = sys.argv[1]

        if command == 'generate-model':
            generate_model(output_name=sys.argv[2])

        elif command == 'download-random-images':
            download_random_images(
                how_much=int(sys.argv[2]),
                folder_path=sys.argv[3],
                initial_index=int(sys.argv[4]),
            )

        elif command == 'get-model-statistics':
            get_model_statistics()

        elif command == 'filler-unsuitable-images':
            filler_unsuitable_images(
                dirpath=sys.argv[2],
                remove='--remove' in sys.argv,
            )

        else:
            print(f'No such command: {command}.')

    except IndexError:
        print('No command has been provided.')
