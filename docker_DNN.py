import tensorflow as tf
import pandas as pd
import numpy as np

from numpy import argmax
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

data = pd.read_csv("test2.csv")
X = data.values[:, :data.shape[1] - 1]
y = data.values[:, data.shape[1] - 1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=y, random_state=777)

model = Sequential()
model.add(Dense(15, activation="relu", kernel_initializer="random_uniform",
                kernel_regularizer=tf.keras.regularizers.L1L2(0.08)
                , input_dim=32))
model.add(Dense(10, activation="relu",kernel_regularizer=tf.keras.regularizers.L1L2(0.08)
                , kernel_initializer="random_uniform"))
model.add(Dense(10, activation="relu",kernel_regularizer=tf.keras.regularizers.L1L2(0.08)
                , kernel_initializer="random_uniform"))
model.add(Dense(10, activation="relu",kernel_regularizer=tf.keras.regularizers.L1L2(0.08)
                , kernel_initializer="random_uniform"))
model.add(Dense(10, activation="relu",kernel_regularizer=tf.keras.regularizers.L1L2(0.08)
                , kernel_initializer="random_uniform"))
model.add(Dense(1, kernel_regularizer=tf.keras.regularizers.L1L2(0.09)
                , activation="sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["acc"])
model.fit(X_train, y_train, epochs=10, batch_size=100, verbose=3, validation_data=(X_test, y_test))
print("acc > {}".format(model.evaluate(X_test, y_test)))
model.save("test_docker_dnn.h5")
test = model.predict_classes(X_test)
print(test)
# 5. 모델 평가하기
loss_and_metrics = model.evaluate(X_test, y_test, batch_size=10)
print('')
print('loss_and_metrics : ' + str(loss_and_metrics))


