import keras
import tensorflow

model = keras.models.load_model("second_try.h5")


def predict(image):
    img_array = tensorflow.keras.utils.img_to_array(image)
    img_array = tensorflow.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    print(predictions)


if __name__ == '__main__':
    img = tensorflow.keras.utils.load_img(
        "dfsf3332d23.jfif",
        target_size=(150, 150),
    )
    predict(img)
