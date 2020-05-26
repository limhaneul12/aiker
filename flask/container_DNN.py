import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.preprocessing import StandardScaler # normalization
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Dropout
from keras.models import Sequential
# 이후 라이브러리 좀 더 추가

# numpy, tensorflow seed 초기화 (동일한 출력값을 얻기 위해)
seed = 0
np.random.seed(seed)
tf.set_random_seed(seed)

data = pd.read_parquet(" ")  # 저장소 불러오기
X = data.values[:, :data.shape[1] - 1]
y = data.values[:, data.shape[1] - 1]
X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
# X, y 값 분류 후 X_Train, y_train 설정 test_size = 0.3 으로 고정값이나 data_size 의 따라
# 바꿀 수 있음

# 정규화 진행
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

# 은닉층 설계 현재로선 4개층이지만 수정 가능
model = Sequential()
model.add(Dense(20, input_dim=31, activation="sigmoid"))
model.add(Dense(10, activation=tf.nn.leaky_relu))
model.add(Dense(10, activation=tf.nn.leaky_relu))
model.add(Dense("", activation="softplus")) # output 은 데이터 칼럼에맞춰서 설정
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["acc"])
model.summary()

history = model.fit(X_train_std, y_train,
                    validation_data=(X_test_std, y_test), epochs=800, batch_size=150)

# 성능 표
print("sample_DNN_train of acc > %.1f" % (model.evaluate(X_train_std, y_train)[1]*100))
print("sample_DNN_test of acc > %.1f" % (model.evaluate(X_test_std, y_test)[1]*100))
