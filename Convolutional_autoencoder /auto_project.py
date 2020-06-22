import tensorflow as tf
import numpy as np

from keras.models import Model, Sequential, Input
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D
from keras.layers import UpSampling2D, Flatten
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model

# 고정된 출력값을 보장하기 위해 seed 고정값을 0으로 설정
np.random.seed(0)
tf.set_random_seed(0)
# 추출 할려는 images shape 값을 임의로 설정
# class 로 객체 설정하면 좀더 유연한 데이터셋을 맞출 수 있을까 생각(개인적)
# 현재로선 mnist 규격인 28,28 로 하여 총 784의 shape을 맞춤 28, 28 (1) -> gray
input_images = Input(shape=(28, 28, 1))

# model 구축 시작
"""
현재 이 모델의 구성도
1. Conv2D --> MaxPooling2D --> Conv2D --> MaxPooling2D --> Conv2D --> MaxPooling2D (encoded)
2. Dense --> Dense -> 실패
3. Conv2D --> Upsampling2D --> Conv2D --> Upsampling2D --> Conv2D -->  Upsampling2D --> Conv2D(decoded) --> OUTPUT

요약
input == > encoded -- (Dense) -- Decoded ==> input

flatten 으로 맞춰야 할 명분이 조금 생긴거 같음
이 모델의 약점은 Dense 의 대한 2차원 또는 1차원으로 모델이 구분 된다면
input data 초기 noise 가 다시 생기거나 없어졌다도 Dense의 noise 가 다시 생길 가능성 이 있음
"""
## function 으로 만들어 보겟음 한번
# encoded
model = (Conv2D(16, kernel_size=(3, 3), activation="relu", padding="same"))(input_images)
model = (MaxPooling2D(2, 2, padding="same"))(model)
model = (Conv2D(8, kernel_size=(3, 3), activation="relu", padding="same"))(model)
model = (MaxPooling2D(2, 2, padding="same"))(model)
model = (Conv2D(8, kernel_size=(3, 3), activation="relu", padding="same"))(model)
encoded = (MaxPooling2D(2, 2, padding="same"))(model)

# 실험으로 encoded - Dense - decoded setting 해봄
# D_model = (Dense(50, activation="relu"))(encoded)
# D_model = (Dense(50, activation="relu"))(D_model)

# decoded
model = (Conv2D(8, kernel_size=(3, 3), activation="relu", padding="same"))(encoded)
model = (UpSampling2D((2, 2)))(model)
model = (Conv2D(8, kernel_size=(3, 3), activation="relu", padding="same"))(model)
model = (UpSampling2D((2, 2)))(model)
model = (Conv2D(16, kernel_size=(3, 3), activation="relu"))(model)
model = (UpSampling2D((2, 2)))(model)
decoded = (Conv2D(1, kernel_size=(3, 3), activation="sigmoid", padding="same", name="A_output"))(model)
"""
일단 CNN 기본 설계 
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
"""
auto_CNN = Model(input_images, decoded)
auto_CNN.compile(optimizer="adadelta", loss="binary_crossentropy")
auto_CNN.summary()
plot_model(auto_CNN, to_file="model.png", show_shapes=True)
