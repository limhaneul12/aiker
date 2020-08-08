import docker
import json
import pandas as pd

"""
1. 로그인 작업해야함 
2. DNN 설계(과적합 방지) 
"""
def create_docker():
    result = []
    #docker remote API와 통신할 길 뚫는 작업
    global pd_arch, container
    client = docker.APIClient(base_url='tcp://0.0.0.0:4323')

    # docker hub에서 이미지 다운 여기서 먼저 이미지 다운 받을 것
    while True:
        image = input("download image > ")
        command = input("command > ")
        name = input("name > ")
        for line in client.pull(image, stream=True):
            print(json.dumps(json.loads(line), indent=4))
            # container 생성
        container = client.create_container(image=image, command=command, name=name)
        print(container)

        container_inspect = client.containers(latest=True)
        print(container_inspect)
        Id = container_inspect[0]["Id"]
        Name = container_inspect[0]["Names"]
        Image = container_inspect[0]["Image"]
        port = container_inspect[0]["Ports"]
        Command = container_inspect[0]["Command"]
        data_save = [Id, Name, Image, port, Command]
    # 재시도 할것인지
        continue_ = input("continue? > ")
        # 끝나면 데이터셋 생성
        if continue_ in ["No", "n", "no", "exit", "false"]:
            result.append(data_save)
            pd_arch = pd.DataFrame(result, columns=['Id', 'Name', 'Image', 'port', 'Command'])
            print(pd_arch)
            pd_arch.to_csv("test.csv", index=False)
            break
        # 계속 할시 list에 담아두고 계속 생성
        elif continue_ in ["yes", "y"]:
            result.append(data_save)
            continue

    return pd_arch




if __name__ == "__main__":
    create_docker()
