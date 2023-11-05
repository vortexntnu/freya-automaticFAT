from src.tools.file_tools import read_yaml
from src.tools.rich_print import generate_print
from src.validations.yaml_validations import config_yamVal

import fire
import time


def main() -> None:
    fats = [
        {"name": "DevOps", "status": "Unknow"},
        {"name": "SITWAS", "status": "Unknow"},
        {"name": "Autonomus", "status": "Unknow"},
        {"name": "Embedded", "status": "Unknow"}
    ]

    status, progress, log = generate_print(fats)

    log.info("Read config file")
    config = read_yaml("config.yaml")
    
    log.info("Validate config file")
    val = config_yamVal(config, log)
    log.info("Finish validating config")

    # if validation failes
    if not val:
        log.error("Exits program")
        return
    
    progress.update("AFAT", advance=1)
    
    


if __name__ == "__main__":
    fire.Fire(main)