import docker
import string
import pandas as pd
"""
pandas -> DataFrame 만들기 위한 장치
string -> 전처리(containers.list --> 이 당시 나의 도커 일련 번호[<Container: b039b77148>, <Container: afceb74e10>]
          형태로 반환이 되므로 list 해체 및 <,> " " 등 빈값 해체 하여 순수 컨테이너 넘버만 추출하겟금 만들기 위한 장치
docker -> docker 진입
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
    for event in container:
        data_change = str(event)
        data_change = data_change.strip("Container<>:")
        finally_data = data_change.strip(string.punctuation + " ")
        container_inspect = client.api.inspect_container(container=finally_data)

if __name__ == "__main__":
    print("container ->", docker_information())