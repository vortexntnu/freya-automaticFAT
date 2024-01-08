from src.tools.file_tools import read_yaml
from src.tools.rich_print import generate_print
from src.validations.yaml_validations import config_yamVal

import fire
import time

from time import sleep

from rich import print
from rich.panel import Panel
from rich.progress import (Progress, BarColumn, TextColumn, TaskProgressColumn, TimeElapsedColumn)
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.logging import RichHandler

import logging


def main() -> None:

    # ------------------------------------------------------
    # init
    # ------------------------------------------------------

    # log
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", 
        format=FORMAT, 
        datefmt="[%X]", 
        handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")
    
    log.info("Read config file")
    config = read_yaml("config.yaml")
    
    # progress bar
    progress = Progress(
        TextColumn("Automatic FAT"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        TimeElapsedColumn()
    )
    # TODO: update with config
    task = progress.add_task("AFAT", total=10)

    # TODO: update with config
    status = [
        {"name": "DevOps", "status": "Unknow"},
        {"name": "SITWAS", "status": "Unknow"},
        {"name": "Autonomus", "status": "Unknow"},
        {"name": "Embedded", "status": "Unknow"}
    ]

    layout = generate_print(status, log, progress)

    # ------------------------------------------------------
    # begining
    # ------------------------------------------------------
    
    with Live(layout, refresh_per_second=10):
        print(layout.tree)
        layout["upper"]["overview"]

        log.info("Read config file")
        config = read_yaml("config.yaml")
        
        log.info("Validate config file")
        val = config_yamVal(config, log)
        log.info("Finish validating config")

        # if validation failes
        if not val:
            log.error("Exits program")
            return
        
        status[0]["status"] = "Fini"
        
        log.info(f"Progress tasks: {progress.tasks}")
        
        for i in range(0, 10):
            progress.update(task, advance=1)
            sleep(.5)
        
        log.info(f"Progress tasks: {progress.tasks}")


if __name__ == "__main__":
    fire.Fire(main)