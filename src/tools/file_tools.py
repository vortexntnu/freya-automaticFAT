from src.tools.rich_print import log_level, fat_status
from src.validations.yaml_validations import fat_yamVal

from dotenv import load_dotenv
from pathlib import Path
import os
import yaml

from rich.console import Console


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
    for file in os.listdir(dir_path):
        if file.endswith(suffix):
            files.append(file)

    return files


# Finds all FATs in directory, read and sort them after priority
def get_fat(devices: dict, console: Console) -> dict | list:
    status = []

    # access test dir
    testDir = get_abs_path("tests")
    fats = filetypeindir(testDir, "")

    # Ask for which fat to run
    if fats:
        p_str = "Found FATs = [ "
        for i in range(0, len(fats)): 
            p_str += f"{i}: {fats[i]}, "
        console.log(f"{log_level['info']} {p_str} ]")
        console.print("\t\t[bright_yellow]    Choose one of the available FATs(index/key):[/bright_yellow]", end=" ")
        fat = int(input(""))
    else:
        console.log(f"{log_level['error']} Can't find any FATs.")
        return []

    # identify scripts in fat and validate
    fatDir = os.path.join(testDir, fats[fat])
    files = filetypeindir(fatDir, ".yaml")
    for file in files:
        file = os.path.join(fatDir, file)
        fat = read_yaml(file)
        valid, msg = fat_yamVal(fat, devices)

        if not valid:
            console.log(f"{log_level['warning']} Found FAT: {file}, however it is invalid: {msg}")
        else:
            console.log(f"{log_level['info']} Found FAT: {file}")
            status.append({"name":    fat["name"],
                           "status":  fat_status["pending"], 
                           "file":    file, 
                           "content": fat})
    
    # sort FATs by priority
    x = 0
    while x < (len(status) - 1):
        y = len(status) - 1

        while y > x:
            pri_x = [status[x]["content"]["priority"] if "priority" in status[x]["content"] else 0]
            pri_y = [status[y]["content"]["priority"] if "priority" in status[y]["content"] else 0]

            if pri_y > pri_x:
                temp = status[x]
                status[x] = status[y]
                status[y] = temp
            
            y -= 1
        x += 1

    return status