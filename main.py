from src.tools.file_tools import read_yaml
from src.tools.rich_print import generate_print
from src.validations.yaml_validations import config_yamVal

import fire
import time

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

    console.rule("Autonomus FAT, Freya")
    
    console.log(f"{log_level['info']} Reading config file")
    config = read_yaml("config.yaml")
    
    console.log(f"{log_level['info']} Applying config file")
    
    devices = {}
    for device in config["autofat"]["network"]:
        devices[device["name"]] = {"ip": device["ip"], "user": device["credientials"]["user"], "pwd": device["credientials"]["pwd"]}

    console.log(devices)
    

    # TODO: update with config
    status = [
        {"name": "DevOps", "status": "Unknow", "file": "Unknow", "fat": object},
        {"name": "SITWAS", "status": "Unknow"},
        {"name": "Autonomus", "status": "Unknow"},
        {"name": "Embedded", "status": "Unknow"}
    ]

    # ------------------------------------------------------
    # begining
    # ------------------------------------------------------
        
    console.log(f"{log_level['info']} Validate config file")
    # val = config_yamVal(config, console)
    console.log(f"{log_level['info']} Finish validating config")


    # ------------------------------------------------------
    # End
    # ------------------------------------------------------    

    console.rule("Summary")

    table = Table(box=box.MINIMAL)

    table.add_column("FAT", justify="left", min_width=20)
    table.add_column("Status", justify="right")

    for row in status:  
        table.add_row(row["name"], row["status"])

    console.print(table)




if __name__ == "__main__":
    fire.Fire(main)