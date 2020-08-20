import docker 
import pandas as pd

client = docker.from_env()

containers = client.containers.list(all=True)
for container in containers:
    result = []
    container_id = container.id
    container_inspect = client.api.inspect_container(container=container_id)
    print(container_inspect)
    Id = container_inspect["Id"]
    Name = container_inspect["Name"]
    Image = container_inspect["Image"]
    port = container_inspect["NetworkSettings"]["Ports"]
    Command = container_inspect["Command"]
    data_save = [Id, Name, Command, port, Image]
    # 끝나면 데이터셋 생성
    
    result.append(data_save)
    
    pd_arch = pd.DataFrame(result, columns=['Id', 'Name', 'Command', 'port', 'Image'])
    print(pd_arch)

    save_dataset = pd_arch.to_csv("dataset_test1.csv", index=False)
    print(save_dataset)

