from src.tools.file_tools import read_yaml, get_fat
from src.tools.cli_tools import ssh_wrap
from src.tools.task_tools import run_task
from src.tools.rich_print import log_level, fat_status
from src.validations.yaml_validations import config_yamVal

import fire
from datetime import datetime

from rich import box
from rich.console import Console
from rich.table import Table


def main() -> None:

    # ------------------------------------------------------
    # init
    # ------------------------------------------------------

    # create console
    console = Console()

    console.rule(f"Automatic FAT, {datetime.now()}")
    
    # read and validate config
    config = read_yaml("config.yaml")
    if config_yamVal(config, console):
        console.log(f"{log_level['info']} Applying config file")
    else:
        console.log(f"{log_level['error']} Config did not pass validation"); return
    
    # use config to identify devices
    devices = {}
    for device in config["autofat"]["network"]:
        devices[device["name"]] = {"ip": device["ip"], "user": device["credentials"]["user"], "pwd": device["credentials"]["pwd"]}
    
    # search for avaliable yaml files in /FATs, they are assumed to be FATs
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
    if status:
        console.rule("Summary")

        # create table of all FATs and their "end" statuses
        table = Table(box=box.MINIMAL)

        table.add_column("File", justify="left")
        table.add_column("FAT", justify="left", min_width=20)
        table.add_column("Status", justify="right")

        for row in status:  
            table.add_row(row["file"], row["name"], row["status"])

        console.print(table)




if __name__ == "__main__":
    fire.Fire(main)