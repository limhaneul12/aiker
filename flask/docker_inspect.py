import docker
import string
import numpy as np
import pandas as pd

client = docker.from_env()
container = client.containers.list(all=True)

for event in container:
    data_change = str(event)
    data_change = data_change.strip("Container<>:")
    finally_data = data_change.strip(string.punctuation + " ")
    container_inspect = client.api.inspect_container(finally_data)

