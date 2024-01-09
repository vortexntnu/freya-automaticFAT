from src.tools.file_tools import read_yaml, filetypeindir, get_abs_path, get_project_path
from src.tools.rich_print import generate_print
from src.validations.yaml_validations import config_yamVal

import fire
import time
import logging as log

from rich import print, box
from rich.console import Console
from rich.table import Table


log_level = {
    "info": "[blue]info[/blue]\t",
    "warning": "[yellow]warning[/yellow]\t",
    "error": "[red]error[/red]\t" ,
}

def main() -> None:

    # ------------------------------------------------------
    # init
    # ------------------------------------------------------

    console = Console()

    console.rule("Autonomous FAT, Freya")
    
    console.log(f"{log_level['info']} Reading config file")
    config = read_yaml("config.yaml")



    devices = {}
    for device in config["autofat"]["network"]:
        devices[device["name"]] = {"ip": device["ip"], "user": device["credentials"]["user"], "pwd": device["credentials"]["pwd"]}

    console.log(devices)
    

    # TODO: update with config
    status = []

    # access FAT dir, add all yaml-files and insert into status
    projectDir = get_project_path()
    fatDir = get_abs_path("/FATs")
    totalDir = projectDir + fatDir
    files = filetypeindir(totalDir, ".yaml")
    for file in files:
        status.append({"name": "Name pending", 
                       "status": "Pending", 
                       "file": file, 
                       "fat": read_yaml(totalDir + "/" + file)})

    

    print(status)

    # ------------------------------------------------------
    # Beginning
    # ------------------------------------------------------
        
    console.log(f"{log_level['info']} Validating config file")
    # Validate config file
    if config_yamVal(config, log):
        console.log(f"{log_level['info']} Finished validating config file")
    else:
        console.log(f"{log_level['error']} Could not validate config file")


    # ------------------------------------------------------
    # End
    # ------------------------------------------------------    

    console.rule("Summary")

    table = Table(box=box.MINIMAL)

    table.add_column("FAT", justify="left", min_width=20)
    table.add_column("Status", justify="center")
    table.add_column("File", justify="right")

    for row in status:  
        table.add_row(row["name"], row["status"], row["file"])

    console.print(table)




if __name__ == "__main__":
    fire.Fire(main)