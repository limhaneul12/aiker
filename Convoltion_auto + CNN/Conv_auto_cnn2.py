import auto_project as auto
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.utils import to_categorical
# mnist dataset 으로 실험 해봄 현재 98% 성능 나옴
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))  # 'channels_firtst'이미지 데이터 형식을 사용하는 경우 이를 적용
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))  # 'channels_firtst'이미지 데이터 형식을 사용하는 경우 이를 적용

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

if __name__ == "__main__":
    history = auto.convolution_auto_model().fit(x_train, y_train,
                                                batch_size=128, epochs=1, shuffle=True,
                                                validation_data=(x_test, y_test), verbose=1)

    # cnn_his = auto.convolution_NN().fit(x_train, y_train,
    #                                    batch_size=128, epochs=1, shuffle=True,
    #                                    validation_data=(x_test, y_test), verbose=1)
    y_vloss = history.history['val_loss']
    y_loss = history.history['loss']

    x_len = np.arange(len(y_loss))
    plt.plot(x_len, y_loss, marker='.', c='blue', label="Train-set Loss")
    plt.plot(x_len, y_vloss, marker='.', c='red', label="Validation-set Loss")

    plt.legend(loc='upper right')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.show()

    decoded_images = auto.convolution_auto_model().predict(x_test)
    n = 10
    plt.figure(figsize=(20, 4))
    for i in range(n):
        # 원본 출력
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(x_test[i].reshape(28, 28))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # 재구성본 출력
        ax = plt.subplot(2, n, i + n)
        plt.imshow(decoded_images[i].reshape(28, 28))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.show()