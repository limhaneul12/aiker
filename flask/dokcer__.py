import docker
import string


def docker_information():
    client = docker.from_env()
    container = client.containers.list(all=True)
    return container


def docker_container_cleaner():
    container = docker_information()
    for event in container:
        data_change = str(event)
        data_change = data_change.strip("Container<>:")
        finally_data = data_change.strip(string.punctuation + " ")

        return finally_data
    

def docker_container_inspect():
    container_load = docker_container_cleaner()
    client = docker.from_env()
    container_inspect = client.api.inspect_container(container=container_load)

    return container_inspect


if __name__ == "__main__":
    print(docker_container_inspect())

    for i in docker_container_inspect():
        print(i)