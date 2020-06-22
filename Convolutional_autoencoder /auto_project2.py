import auto_project as auto
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from keras.models import load_model
from keras.utils import to_categorical
from keras.datasets import mnist
from numpy import argmax
"""
-- 주의 사항 -- 
이 모델을 철저히 classification 의 초점 으로 맞춰저 있지 않음
unsupervised learning 을 preprocessing 으로 초점이 맞춰서 있음 
############################################################
현재 목표 
Convolution AutoEncoder  ->  Convolution Neural Network
############################################################
mnist 로 학습을 진행한 이유는 
해당 모델의 특징추출이 되는지 확인 후
데이터셋를 맞출 예정임
"""
# 고정된 출력값을 보장하기 위해 seed 고정값을 0으로 설정
tf.set_random_seed(0)
np.random.seed(0)

# mnist dataset 의 간단한 데이터 전처리
# (x_train, y_train), (x_test, y_test) = mnist.load_data()
(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))  # 'channels_firtst'이미지 데이터 형식을 사용하는 경우 이를 적용
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))  # 'channels_firtst'이미지 데이터 형식을 사용하는 경우 이를 적용
print(x_train.shape)
print(x_test.shape)

if __name__ == "__main__":
    # fit(학습 주기) 선택
    history = auto.auto_CNN.fit(x_train, x_train,
                                batch_size=128, epochs=50, shuffle=True,
                                validation_data=(x_test, x_test), verbose=1)
    auto.auto_CNN.save("Convolution_Autoencoder_Mnist_ver3_Non_Dense.h5")
    # cnn_his = auto.convolution_NN().fit(x_train, y_train,
    #                                    batch_size=128, epochs=1, shuffle=True,
    # 보류                                validation_data=(x_test, y_test), verbose=1)

    # 각 loss, validation_loss 의 그래프 시각화
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
    # 여기 까지 성능 그래프 시각화
    """
    xhat_idx = np.random.choice(x_test.shape[0], 60000)
    xhat = x_test[xhat_idx]
    yhat = auto.convolution_auto_model().predict(xhat)
    
    result = 0
    loss = 0
    for i in range(60000):
        # print('True : ' + str(argmax(y_test[xhat_idx[i]])) + ', Predict : ' + str(yhat[i]))
        if str(argmax(x_test[xhat_idx[i]])) == str(yhat[i]):
            result += 1
        elif str(argmax(x_test[xhat_idx[i]])) != str(yhat[i]):
            loss += 1
        else:
            print("errors")
    print("result > " + str(result) + " loss > ", str(loss))
    """
    #decoded 까지 학습이 다 끝나면 예상값을 x_test 값으로맞춤
    decoded_images = auto.convolution_auto_model().predict(x_test)
    n = 10 # 총 10개의 test image visualization
    plt.figure(figsize=(20, 4)) # 규격 설정
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

