import docker
import socket #차후 nodejs로 도커 id받아오는 작업
import sqlite3

def docker_container_inspect():

    client = docker.from_env()
    containers = client.containers.list(all=True)

    list = {}

    for container in containers:
        i = 0

        container_id = container.id

        container_inspect = client.api.inspect_container(container=container_id)

        container_name = container_inspect['Name']
        container_image = container_inspect['Image']

        list = {'{}'.format(i) : container_id + ' ' + container_name + ' ' + container_image}
        #{'0': '60edf341d2d3f2e2e9b8ab3125022db04878ab799ab683e67344753fc4efded0 /docker-tutorial sha256:cb1386417d5cdc5464db23eec9acb86b64d052894abe5c3a051f9e1e6b13d5a9'}

        i += 1
    return list





if __name__ == "__main__":
    print(docker_container_inspect())