from rich import box
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
import logging


def generate_print(status: dict | list, log: logging.Logger, progress: Progress) -> Layout:
    table = Table(box=box.SIMPLE)
    table.add_column("Status")
    table.add_column("FAT")

    for fat in status:
        table.add_row(
            f"{fat['status']}", f"{fat['name']}"
        )

    root = Layout()

    root.split_column(
        Layout(name="upper"),
        Layout(progress, name="progress")
    )

    root["upper"].split_row(
        Layout(table, name="overview"),
        Layout(name="log")
    )

    return root