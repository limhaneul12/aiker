import docker
import string
import sys # 모듈 추가 2020/07/03 PM 19시 17분
import pandas as pd
import numpy as np

from numpy import argmax
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

"""
pandas -> DataFrame 만들기 위한 장치
string -> 전처리(containers.list --> 이 당시 나의 도커 일련 번호[<Container: b039b77148>, <Container: afceb74e10>]
          형태로 반환이 되므로 list 해체 및 <,> " " 등 빈값 해체 하여 순수 컨테이너 넘버만 추출하겟금 만들기 위한 장치
docker -> docker 진입
2020/07/03
sys 모듈 추가 
sys -> sys 모듈은 파이썬 인터프리터가 제공하는 변수와 함수를 직접 제어할 수 있게 해주는 모듈
       내부에서 쓸수 있는 함수를 우리가 직접 제어할 수 있음. 
"""

# docker container 접근하기 위한 function
def docker_information():
    # docker 데몬(명령프롬프트)에 접근
    client = docker.from_env()
    # container list 추출 --> (docker ps -a)
    container = client.containers.list(all=True)
    return container

# [<Container: b039b77148>, <Container: afceb74e10>]
# 순수한 일련 번호 추출을 위한 전처리 과정 b039b77148, afceb74e10
def docker_container_cleaner():
    # docker_information 의 결과값을 가져옴
    container = docker_information()
    # docker 데몬(명령프롬프트)에 접근
    client = docker.from_env()
    """
    반복할 수 있는 겍체를 container 로 설정 하고 
    for 반복문을 돌림
    
    우리는 b039b77148, afceb74e10 이렇게 순수한 일련번호의 값을 추출할것이기에
    해당 컨데이터를 문자열로 변환 후 strip 기능 사용해서 쓸모없는 문자와 빈칸을 제거
    
    그다음 해당 각 컨데이너 마다 값을 추출하기 위해 데몬 접근해서 inspect_container 사용 
     container_inspect --> (docker inspect <container name or number>)
    """
    output = [] # 추가 부분 2020/07/01 PM 19:25
    for event in container:
        data_change = str(event)
        data_change = data_change.strip("Container<>:")
        finally_data = data_change.strip(string.punctuation + " ")
        container_inspect = client.api.inspect_container(container=finally_data)
        output.append(container_inspect) # 추가 부분 2020/07/01 PM 19:25
    return output # 추가 부분 2020/07/01 PM 19:25

if __name__ == "__main__":
    # 새롭게 만듬 python (node_js 로 데이터를 보내는쪽) 
    # 나는 이렇게 작성했으나 원했던 니즈가 아닐 수 있음 절대적 지표는 아니기에 분석 후 재수정 요망
    """
     2020/07/03 PM 19시 17분 추가 
    """
    docker_container_cleaner() 
    data1 = sys.argv # argv[변수를 담을 수 있는 공간] 데이터 타입이 list 타입인걸 확인 
    data2 = data1 + list(docker_container_cleaner()) # docker_container_cleaner() 함수를 리스트화 시켜 argv 화 합병
    print("------------------------------------------------------------------------------------------------------------------------------")
    print(data2)
    id = data2[1]['Id']
    name = data2[1]['Name']
    port = data2[1]["NetworkSettings"]['Ports']
    command = data2[1]["Config"]['Cmd']
    image = data2[1]["Config"]['Image']

    result = []
    data_save = [id, name, port, command, image]
    result.append(data_save)
    pd_arch = pd.DataFrame(result, columns=['ID', 'name', 'port', 'command', 'image'])
    print(pd_arch)
