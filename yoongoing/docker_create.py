import docker
import pandas as pd
import numpy as np
import json
import pymysql

from numpy import argmax
from http.server import BaseHTTPRequestHandler, HTTPServer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import LabelEncoder


port = 8000


class my_handler(BaseHTTPRequestHandler):

    def _set_header(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()


    def _set_key_value(self, lists):
        set = {}

        for list in lists:
            temp = list.split('=')
            set[temp[0]] = temp[1]

        return set

    def create_docker(self, name, image, port, command):
        result = []
        
        # docker remote API와 통신할 길 뚫는 작업
        global pd_arch, container
        client = docker.APIClient(base_url='tcp://0.0.0.0:4323')

        # docker hub에서 이미지 다운 여기서 먼저 이미지 다운 받을 것
        for line in client.pull(image, stream=True):
            print(json.dumps(json.loads(line), indent=4))
        
        # container 생성
        container = client.create_container(image=image, command=command, name=name)
        print(container)

        container_inspect = client.containers(latest=True)
        print(container_inspect)
        ID = container_inspect[0]["Id"]    
        data_save = [ID, name, port, command, image]
        
        # 끝나면 데이터셋 생성
        result.append(data_save)
        
        pd_arch = pd.DataFrame(result, columns=['ID', 'name', 'port', 'command', 'image'])
        print(pd_arch)
        
        csv = pd_arch.to_csv("test.csv", index=False)
        data = self.preprocessing(csv)
        result = self.DNN(data)

        return ID, result

    def preprocessing(self, csv):
        
        data = pd.read_csv('/home/limsky/PycharmProjects/Deeplearning/test.csv')
        data_ndim = np.ndim(data)
        print("data_ndim > {}".format(data_ndim))

        x = data.iloc[:, :-1].values
        y = data.iloc[:, 4].values

        le = LabelEncoder()
        id_label = x[:, 0] = le.fit_transform(x[:, 0])
        name_label = x[:, 1] = le.fit_transform(x[:, 1])
        image_label = x[:, 2] = le.fit_transform(x[:, 2])
        command_label = y[:] = le.fit_transform(y[:])

        print("Id labelencoder > {}".format(id_label))
        print("name labelencoder > {}".format(name_label))
        print("command_label > {}".format(command_label))
        print("image_label > {}".format(image_label))
        print(data.shape)
        
        return data

    def DNN(self, data):
        
        X = data.values[:, :data.shape[1] - 1]
        y = data.values[:, data.shape[1] - 1]
        model = Sequential()
        model.add(Dense(5, activation="relu", input_dim=4))
        model.add(Dense(2, activation="relu"))
        model.add(Dense(2, activation="relu"))
        model.add(Dense(2, activation="relu"))
        model.add(Dense(1, activation="sigmoid"))

        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["acc"])
        model.fit(X, y, epochs=100, batch_size=1, verbose=1)
        print("acc: {} ".format(model.evaluate(X, y)))
        
        pred = model.predict_classes(X)
        print(pred)
        
        xhat_idx = np.random.choice(X.shape[0], 1)
        xhat =  X[xhat_idx]
        yhat = model.predict_classes(xhat)

        result = 0
        loss = 0
        for i in range(xhat):
             if str(argmax(y_test[xhat_idx[i]])) == str(yhat[i]):
                result += 1
             elif str(argmax(y_test[xhat_idx[i]])) != str(yhat[i]):
                loss += 1
        print("result >", result, "loss >", loss)

        return result  

    #create
    def do_POST(self):
        self._set_header()

        path = self.path
        if '?' in self.path:
            urls = self.path.split('?')
            request = urls[0]
            kv = urls[1].split('&')

        kv = self._set_key_value(kv)
        print(kv)


        if(request == '/create_docker'):
            ID, result = self.create_docker(kv['name'], kv['image'], kv['port'], kv['command'])
            conn = pymysql.connect(host='db-4l33j.pub-cdb.ntruss.com', user='aiker', password='aiker1234*', charset='utf8',database='aiker')
            cursor = conn.cursor()

            sql = "insert into docker (ID,name,image,port,command,label_idx,user_idx) values ('{}','{}','{}','{}','{}',{},{})"\
                .format(ID, kv['name'], kv['image'], kv['port'], kv['command'], result, kv['user_idx'])

            cursor.execute(sql)

            conn.commit()
            conn.close()







httpd = HTTPServer(('localhost', port), my_handler)
print('Server running on port : 8000')
httpd.serve_forever()



`WQ!
