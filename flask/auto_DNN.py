import pandas as pd
import numpy as np
import tensorflow as tf
import sys

from sklearn.preprocessing import StandardScaler # normalization
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Dropout
from keras.models import Sequential
from tensorflow.contrib.labeled_tensor import shuffle_batch

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


####################
# layer params #
####################
noise_level = 1.0
n_inputs = 23
n_hidden1 = 1000
n_outputs = 1


####################
# train params #
####################
sparsity_target = 0.1 # p
sparsity_weight = 0.2
learning_rate = 0.01
n_epochs = 200
batch_size = 100

def kl_divergence(p, q):
    # 쿨백 라이블러 발산
    return p * tf.log(p / q) + (1 - p) * tf.log((1 - p) / (1 - q))

inputs = tf.placeholder(tf.float32, shape=[None, n_inputs])

hidden1 = tf.layers.dense(inputs, n_hidden1, activation=tf.nn.sigmoid)
outputs = tf.layers.dense(hidden1, n_outputs)

# loss
hidden1_mean = tf.reduce_mean(hidden1, axis=0)  # 배치 평균  == q
sparsity_loss = tf.reduce_sum(kl_divergence(sparsity_target, hidden1_mean))
reconstruction_loss = tf.losses.mean_squared_error(labels=inputs, predictions=outputs)
loss = reconstruction_loss + sparsity_weight * sparsity_loss

# optimizer
train_op = tf.train.AdamOptimizer(learning_rate).minimize(loss)

# saver
saver = tf.train.Saver()

# Train
with tf.Session() as sess:
    tf.global_variables_initializer().run()
    n_batches = len(X_train) // batch_size
    for epoch in range(n_epochs):
        for iteration in range(n_batches):
            print("\r{}%".format(100 * iteration // n_batches), end="")
            sys.stdout.flush()
            batch_x, batch_y = next(shuffle_batch(X_train, y_train, batch_size))
            sess.run(train_op, feed_dict={inputs: batch_x})
        recon_loss_val, sparsity_loss_val, loss_val = sess.run([reconstruction_loss,
                                                                sparsity_loss,
                                                                loss], feed_dict={inputs: batch_x})
        print('\repoch : {}, Train MSE : {:.5f}, \
                sparsity_loss : {:.5f}, total_loss : {:.5f}'.format(epoch, recon_loss_val,
                                                                    sparsity_loss_val, loss_val))
    saver.save(sess, './model/my_model_sparse.parquet')


data_unsupervised = pd.read_parquet(" ")  # 저장소 불러오기
X = data_unsupervised.values[:, :data_unsupervised.shape[1] - 1]
y = data_unsupervised.values[:, data_unsupervised.shape[1] - 1]
X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
# X, y 값 분류 후 X_Train, y_train 설정 test_size = 0.3 으로 고정값이나 data_size 의 따라

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
