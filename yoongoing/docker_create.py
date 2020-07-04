import docker
import json


from docker import DockerClient

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
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    print(client.version())

    #원래는 웹서버로 부터 받아온 인자값으로 넣어야 하지만, 지금은 걍 예시로 넣는 중
    container = client.create_container(
        'busybox', # !!!!!!!!!!!여기에 에러남 왠지 몰겠음!!!!!!!!!!!
        'ls',
        ports=[1111, 2222],
        host_config=client.create_host_config(port_bindings={1111: 4567, 2222: None}))

    print(container)  # 원래대로라면 도커의 정보가 잘~ 나와야함

    #컨테이너를 create_container로 만들면 start를 해줘야 한다고함
    response = client.start(container=container.get('Id'))
    print(response)  # 음 모르겠음


if __name__ == "__main__":
    print(create_docker())