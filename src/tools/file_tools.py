from pathlib import Path
import os

import yaml


# Get absolute path to this project
def get_project_path() -> str:
    return str(Path(__file__).parents[2])


# Convert relative path to absolute path
def get_abs_path(rel_path: str) -> str:
    project_path = get_project_path()
    return os.path.join(project_path, rel_path)


# Reads a yaml file and return the yaml object
def read_yaml(file_path: str) -> dict | list:
    abs_file_path = get_abs_path(file_path)

    with open(abs_file_path, "r") as file:
        yaml_data = yaml.load(file, Loader=yaml.FullLoader)
    
    return yaml_data