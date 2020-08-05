import docker
import json
import pandas as pd

def create_docker():
    '''
    Nodejs로부터 값을 받아오겠죠?
    docker_id = 받아온 id
    docker_name =
    docker_image =
    docker_port =
    docker_command =
    요정도 받아옵시다
    '''

    #docker remote API와 통신할 길 뚫는 작업

    client = docker.APIClient(base_url='tcp://192.168.1.224:4323')

    # docker hub에서 이미지 다운 여기서 먼저 이미지 다운 받을 것
    image_download = input("download image >")
    for line in client.pull(image_download, stream=True):
        print(json.dumps(json.loads(line), indent=4))

    # container 생성
    container = client.create_container(image=image_download, command=input("command >"))
    print(container)
    # 생성된 container inspect
    """
     curl -L http://127.0.1.1:4243/containers/json?all=1      
     
    [{"Id":"ab38a05f8cea8bd853bd132353064fcc70dad1881a971ba45d84704286c836fd",
    "Names":["/silly_tharp"],
    "Image":"busybox:latest",
    "ImageID":"sha256:c7c37e472d31c1685b48f7004fd6a64361c95965587a951692c5f298c6685998",
    "Command":"/bin/sleep 30","Created":1593941327,
    "Ports":[],
    "Labels":{},
    "State":"created",
    "Status":"Created",
    "HostConfig":{"NetworkMode":"default"},
    "NetworkSettings":{"Networks":{"bridge":{"IPAMConfig":null,"Links":null,"Aliases":null,
                        "NetworkID":"","EndpointID":"","Gateway":"","IPAddress":"","IPPrefixLen":0,"IPv6Gateway":"",
                        "GlobalIPv6Address":"","GlobalIPv6PrefixLen":0,"MacAddress":"","DriverOpts":null}}},"Mounts":[]}]

    """
    container_inspect = client.containers(latest=True)

    Id = container_inspect[0]["Id"]
    Name = container_inspect[0]["Names"]
    Image = container_inspect[0]["Image"]
    port = container_inspect[0]["Ports"]
    Command = container_inspect[0]["Command"]
    test_info = [Id, Name, Image, port, Command]
    print(test_info)
    print()

   #데이터셋 만들기 while문으로 조건 반복 실행해서 한번이 아니라 여러 이미지 다운 받을 수 있게 할 수 있을듯 
    pd_arch = pd.DataFrame({"Id": [Id], "Name": [Name], "Image": [Image], "ports": [port], "Command": [Command]})
    pd_arch.to_csv("test.csv", index=False)
    return test_info, pd_arch


if __name__ == "__main__":
    print(create_docker())
