from src.tools.file_tools import read_yaml, get_fat
from src.tools.cli_tools import ssh_wrap
from src.tools.task_tools import run_task
from src.tools.rich_print import log_level, fat_status
from src.validations.yaml_validations import config_yamVal

import fire
import time
from datetime import datetime

from rich import print, box
from rich.console import Console
from rich.table import Table

import fire

status = []

def main() -> None:

    # ------------------------------------------------------
    # init
    # ------------------------------------------------------

    console = Console()

    console.rule(f"Automatic FAT, Freya, {datetime.now()}")
    
    # console.log(f"{log_level['info']} Reading config file")
    config = read_yaml("config.yaml")

    # console.log(f"{log_level['info']} Validate config file")
    if config_yamVal(config, console):
        console.log(f"{log_level['info']} Applying config file")
    else:
        console.log(f"{log_level['error']} Config did not pass validation"); return
    

    # console.log(f"{log_level['info']} Applying config file")
    
    devices = {}
    for device in config["autofat"]["network"]:
        devices[device["name"]] = {"ip": device["ip"], "user": device["credentials"]["user"], "pwd": device["credentials"]["pwd"]}
    
    console.log(f"{log_level['info']} Searching for FATs")

    status = get_fat(devices, console)
    
    console.log(f"{log_level['info']} Initial setup finished")

    # ------------------------------------------------------
    # Loop and do FATs
    # ------------------------------------------------------

    # loop through all fats registered
    for fat in status:
        console.log(f"\n{log_level['info']} Beginning FAT: {fat['name']}")
        fat["status"] = fat_status["running"]

        # loop through all tasks in a fat
        for task in fat["content"]["tasks"]:
            console.log(f"{log_level['info']} Doing task: {task['name']}")

            # if the task should be ran on a different device
            if "device" in task and task["device"] != "laptop":
                task["command"] = ssh_wrap(task["command"], devices[task["device"]])

            # do task, if fail break for-loop
            if not run_task(fat, task, console):
                break
                
        # check fat status 
        if fat["status"] == fat_status["running"]:
            fat["status"] = fat_status["success"]
            console.log(f"{log_level['info']} FAT: {fat['name']}, [green]successful[/green]")  
        else:
            console.log(f"{log_level['info']} FAT: {fat['name']}, [red]failed[/red]")
        
        if fat["status"] == fat_status["failed"] and "priority" in fat["content"]:
            break


    # ------------------------------------------------------
    # End
    # ------------------------------------------------------    

    console.rule("Summary")

    table = Table(box=box.MINIMAL)

    table.add_column("File", justify="left")
    table.add_column("FAT", justify="left", min_width=20)
    table.add_column("Status", justify="right")

    for row in status:  
        table.add_row(row["file"], row["name"], row["status"])

    console.print(table)




if __name__ == "__main__":
    fire.Fire(main)