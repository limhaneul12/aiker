
import pandas as pd
import numpy as np

from numpy import argmax
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

data = pd.read_csv("dataset4.csv")
X = data.values[:, :data.shape[1] - 1]
y = data.values[:, data.shape[1] - 1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=y, random_state=1)

model = Sequential()
model.add(Dense(5, activation="relu", input_dim=28))
model.add(Dense(10, activation="relu"))
model.add(Dense(10, activation="relu"))
model.add(Dense(10, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["acc"])
model.fit(X_train, y_train, epochs=50, batch_size=10, verbose=1, validation_data=(X_test, y_test))
print("acc > {}".format(model.evaluate(X_test, y_test)))
model.save("test_docker_dnn.h5")

# 5. 모델 평가하기
loss_and_metrics = model.evaluate(X_test, y_test, batch_size=10)
print('')
print('loss_and_metrics : ' + str(loss_and_metrics))
