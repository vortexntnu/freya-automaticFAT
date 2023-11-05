from src.tools.file_tools import read_yaml
from src.tools.validate_config import *
from src.tools.validate_fat import *

import fire

def main() -> None:
    config = read_yaml("config.yaml")
    print("hei")
    print(config)

if __name__ == "__main__":
    fire.Fire(main)