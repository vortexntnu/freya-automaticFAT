from rich import print
from rich.panel import Panel
from rich.progress import (Progress, BarColumn, TextColumn, TaskProgressColumn, TimeElapsedColumn)
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.logging import RichHandler

import logging


def generate_print(fats: dict | list) -> tuple[Table, Progress, logging.Logger]:
    # Status table
    status = Table()
    status.add_column("Status")
    status.add_column("FAT")

    for fat in fats:
        status.add_row(
            f"{fat['status']}", f"{fat['name']}"
        )

    # log
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", 
        format=FORMAT, 
        datefmt="[%X]", 
        handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")

    # progress bar
    progress = Progress(
        TextColumn("Automatic FAT"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        TimeElapsedColumn()
    )
    progress.add_task("AFAT", total=1)

    # create layout
    root = Layout()

    root.split_column(
        Layout(name="upper"),
        Layout(progress)
    )

    root["upper"].split_row(
        Layout(status),
        Layout(name="log")
    )

    print(root)

    return (status, progress, log)