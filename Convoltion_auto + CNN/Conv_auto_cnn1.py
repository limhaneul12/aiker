import tensorflow as tf
import numpy as np

from keras.models import Model, Sequential, Input
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D
from keras.layers import UpSampling2D, Flatten
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model

np.random.seed(0)
tf.set_random_seed(0)
input_images = Input(shape=(28, 28, 1))


def convolution_auto_model():
    # encoded
    model = (Conv2D(16, kernel_size=(3, 3), activation="relu", padding="same"))(input_images)
    model = (MaxPooling2D(2, 2, padding="same"))(model)
    model = (Conv2D(8, kernel_size=(3, 3), activation="relu", padding="same"))(model)
    model = (MaxPooling2D(2, 2, padding="same"))(model)
    model = (Conv2D(8, kernel_size=(3, 3), activation="relu", padding="same"))(model)
    encoded = (MaxPooling2D(2, 2, padding="same"))(model)

    # 실험으로 encoded - Dense - decoded setting 해봄
    model = (Dense(50, activation="relu"))(encoded)
    model = (Dense(50, activation="relu"))(model)

    # decoded
    de_model = (Conv2D(8, kernel_size=(3, 3), activation="relu", padding="same"))(model)
    de_model = (UpSampling2D((2, 2)))(de_model)
    de_model = (Conv2D(8, kernel_size=(3, 3), activation="relu", padding="same"))(de_model)
    de_model = (UpSampling2D((2, 2)))(de_model)
    de_model = (Conv2D(16, kernel_size=(3, 3), activation="relu"))(de_model)
    de_model = (UpSampling2D((2, 2)))(de_model)
    decoded = (Conv2D(1, kernel_size=(3, 3), activation="sigmoid", padding="same", name="A_output"))(de_model)

    # conv(relu)-subsampleing-con(relu)-subsampleing
    # 층 설계
    Cmodel = (Conv2D(64, kernel_size=(3, 3), activation="relu", padding="same"))(decoded)
    Cmodel = (MaxPooling2D((2, 2), padding="same"))(Cmodel)
    Cmodel = (Conv2D(64, kernel_size=(3, 3), padding="same"))(Cmodel)
    Cmodel = (MaxPooling2D((2, 2), padding="same"))(Cmodel)
    Cmodel = (Flatten())(Cmodel)
    Cmodel = (Dense(128, activation="relu"))(Cmodel)
    Cmodel = (Dense(64, activation="relu"))(Cmodel)
    Cmodel = (Dropout(0.5))(Cmodel)
    Cmodel = (Dense(30, activation="relu"))(Cmodel)
    Cmodel = (Dense(10, activation="softplus"))(Cmodel)

    auto_CNN = Model(input_images, Cmodel)
    auto_CNN.compile(optimizer="adadelta", loss="categorical_crossentropy",
                     metrics=["accuracy"])
    auto_CNN.summary()
    plot_model(auto_CNN, to_file="model.png", show_shapes=True)
    return auto_CNN

if __name__ == "__main__":
    print("# Convolution autoencoder and Convolution Neural Network")
    print(convolution_auto_model())
"""
def model_fit(train, test,
              batch_size, epochs, verbose, validation_data, shuffle):
    model = convolution_auto_model()
    model.fit(x=train, y=test,
              batch_size=batch_size, epochs=epochs, verbose=verbose,
              validation_data=validation_data, shuffle=shuffle)

    return model_fit
"""