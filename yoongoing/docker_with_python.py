import docker
import string

def docker_information():
    client = docker.from_env()
    print(client)
    container = client.containers.list(all=True)
    return container


def docker_container_cleaner():
    container = docker_information()
    for event in container:
        data_change = str(event)
        #print(data_change)
        data_change = data_change.strip("Container<>:")
        #print(data_change)
        finally_data = data_change.strip(string.punctuation + " ")
        #print(finally_data)
        return finally_data


def docker_container_inspect():
    container_load = docker_container_cleaner()
    client = docker.from_env()

    container_inspect = client.api.inspect_container(container=container_load)
    print(container_inspect)

    container_id = container_inspect['Id']
    #container_id = container_id[:12]

    container_name = container_inspect['Name']

    container_image = container_inspect['Image']
    #container_image = container_image.strip("sha256:")
    #container_image = container_image[:10]

    print(container_id)
    print(container_name)
    print(container_image)

    return container_id, container_name,container_image


if __name__ == "__main__":
    print(docker_container_inspect())