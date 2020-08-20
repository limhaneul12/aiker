import docker
import json
import pandas as pd
import numpy as np

from numpy import argmax
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def create_docker():
    global pd_arch, container, save_dataset
    result = []
    # docker remote API와 통신할 길 뚫는 작업
    client = docker.APIClient(base_url='tcp://0.0.0.0:4323')

    # docker hub에서 이미지 다운 여기서 먼저 이미지 다운 받을 것
    while True:
        image = input("download image > ")
        command = input("command > ")
        name = input("name > ")
        for line in client.pull(image, stream=True, decode=True):
            print(json.dumps(line, indent=4))
            # container 생성

        container = client.create_container(image=image, command=command, name=name, ports=[4323, 8000])

        container_inspect = client.containers(latest=True)
        print(container_inspect)
        Id = container_inspect[0]["Id"]
        Name = container_inspect[0]["Names"]
        Image = container_inspect[0]["Image"]
        port = container_inspect[0]["Ports"]
        Command = container_inspect[0]["Command"]
        data_save = [Id, Name, Command, port, Image]
    # 재시도 할것인지
        continue_ = input("continue? > ")
        # 끝나면 데이터셋 생성
        if continue_ in ["No", "n", "no", "exit", "false"]:
            result.append(data_save)
            pd_arch = pd.DataFrame(result, columns=['Id', 'Name', 'Command', 'port', 'Image'])
            print(pd_arch)
            break
        # 계속 할시 list에 담아두고 계속 생성
        elif continue_ in ["yes", "y"]:
            result.append(data_save)
            continue

    save_dataset = pd_arch.to_csv("dataset_test1.csv", index=False)
    return save_dataset

def preprocessing(data):
    data = pd.read_csv(data)
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

if __name__ == "__main__":
    create_docker()
