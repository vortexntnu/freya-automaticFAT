import fire
import time

from rich.layout import Layout
from rich.table import Table
from rich.live import Live


def update_status(status: dict | list) -> Table:
    table = Table()

    table.add_column("FAT", justify="left")
    table.add_column("Status", justify="right")

    for row in status:
        table.add_row(row["fat"], row["status"])
    
    return table


def main():

    status = [
        {"fat": "DevOps", "status": "[yellow]Running"},
        {"fat": "SITAW", "status": "[yellow]Waiting"}
    ]

    with Live(update_status(status), refresh_per_second=4) as live:
        live.console.log("start")
        
        time.sleep(1)
        status[0]["status"] = "[green]OK"
        status[1]["status"] = "[yellow]Running"
        live.update(update_status(status))

        live.console.log("run X")
        live.console.log("run Y")
        live.console.log("run Z")

        time.sleep(1)
        status[1]["status"] = "[red]Error"
        live.update(update_status(status))   

        live.console.log("[red]Error: noe gikk feil.")

        live.console.print("What is your name?")
        name = live.console.input()
        live.console.log(name)


if __name__ == "__main__":
    fire.Fire(main)