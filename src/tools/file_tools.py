from pathlib import Path
import os

import yaml
from dotenv import load_dotenv


# Get absolute path to this project
def get_project_path() -> str:
    return str(Path(__file__).parents[2])


# Convert relative path to absolute path
def get_abs_path(rel_path: str) -> str:
    project_path = get_project_path()
    return os.path.join(project_path, rel_path)


# Replace placeholders with environment variables
def replace_env_vars(data: dict | list) -> dict | list:
    if isinstance(data, str):
        return os.path.expandvars(data)
    if isinstance(data, dict):
        return {key: replace_env_vars(value) for key, value in data.items()}
    if isinstance(data, list):
        return [replace_env_vars(item) for item in data]
    return data


# Reads a yaml file and return the yaml object
def read_yaml(file_path: str) -> dict | list:
    abs_file_path = get_abs_path(file_path)

    load_dotenv()

    # read yaml file
    with open(abs_file_path, "r") as file:
        yaml_data = yaml.load(file, Loader=yaml.FullLoader)
    
    return replace_env_vars(yaml_data)

# Return a list of files with a given ending
def filetypeindir(dir_path: str, suffix: str) -> list:
    files = []
    for file in os.listdir(get_abs_path(dir_path)):
        if file.endswith(suffix):
            files.append(file)

    return files