import fire
import time

from rich.layout import Layout
from rich.table import Table
from rich.live import Live
from rich.console import Console
from rich import box

from rich.logging import RichHandler

import logging


def generate_status_table(status: dict | list) -> Table:
    table = Table(box=box.MINIMAL)

    table.add_column("FAT", justify="left", min_width=20)
    table.add_column("Status", justify="right")

    for row in status:  
        table.add_row(row["fat"], row["status"])
    
    return table


log_level = {
    "info": "[blue]info[/blue]\t",
    "warning": "[yellow]warning[/yellow]\t",
    "error": "[red]error[/red]\t" ,
}


def main():

    status = [
        {"fat": "DevOps", "status": "[yellow]Running"},
        {"fat": "SITAW", "status": "[yellow]Waiting"}
    ]

    # layout = Layout().split_row(
    #     Layout(name="statues"),
    #     Layout(name="log")
    # )


    console = Console()

    console.print("Automatic FAT, Freya\n")

    a = console.input("start? (Y/n): ")
    console.log(f"{log_level['info']} {a}")
    console.log(f"{log_level['warning']} Hei")

    console.print("\nSummary")

    console.print(generate_status_table(status))


if __name__ == "__main__":
    fire.Fire(main)