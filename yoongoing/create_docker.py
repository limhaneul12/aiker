import docker
import json

from docker import DockerClient

def create_docker():
    client = DockerClient(base_url='tcp://127.0.0.1:2375')

    for line in client.api.pull('busybox', stream=True):
        print(json.dumps(json.loads(line), indent=4))

    container = client.api.create_container(image='busybox:latest', command='/bin/sleep 30')
    print(container)  # {'Id': '8a61192da2b3bb2d922875585e29b74ec0dc4e0117fcbf84c962204e97564cd7', 'Warnings': None}

    response = client.api.start(container=container.get('Id'))
    print(response)  # None


if __name__ == "__main__":
    print(create_docker())