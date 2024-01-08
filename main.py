from src.tools.file_tools import read_yaml
from src.tools.rich_print import generate_print
from src.validations.yaml_validations import config_yamVal

import fire
import time

from rich import print
from rich.console import Console

import logging

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
    
    console.log(f"{log_level['info']} Read config file")
    config = read_yaml("config.yaml")
    

    # TODO: update with config
    status = [
        {"name": "DevOps", "status": "Unknow"},
        {"name": "SITWAS", "status": "Unknow"},
        {"name": "Autonomus", "status": "Unknow"},
        {"name": "Embedded", "status": "Unknow"}
    ]

    # ------------------------------------------------------
    # begining
    # ------------------------------------------------------
        
    console.log(f"{log_level['info']} Validate config file")
    val = config_yamVal(config, console)
    console.log(f"{log_level['info']} Finish validating config")




if __name__ == "__main__":
    fire.Fire(main)