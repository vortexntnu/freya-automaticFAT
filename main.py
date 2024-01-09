from src.tools.file_tools import read_yaml, filetypeindir, get_abs_path, get_project_path
from src.tools.rich_print import generate_print
from src.validations.yaml_validations import config_yamVal
from src.tools.cli_tools import run_bool

from rich import print, box
from rich.console import Console
from rich.table import Table

import fire

log_level = {
    "info": "[blue]info[/blue]\t",
    "warning": "[bright_yellow]warning[/bright_yellow]\t",
    "error": "[red]error[/red]\t" ,
}

fat_status = {
    "pending": "[yellow]pending[/yellow]",
    "running": "[bright_yellow]running[/bright_yellow]",
    "success": "[green]success[/green]",
    "failed": "[red]>failed[/red]"
}

def main() -> None:

    # ------------------------------------------------------
    # init
    # ------------------------------------------------------

    console = Console()

    console.rule("Automatic FAT, Freya")
    
    console.log(f"{log_level['info']} Reading config file")
    config = read_yaml("config.yaml")

    console.log(f"{log_level['info']} Validating config file")
    config_val = True # config_yamVal(config, console) TODO: revisit config validation
    if config_val:
        console.log(f"{log_level['info']} Finished validating config")
    else:
        console.log(f"{log_level['error']} Config did not pass validation")
    

    console.log(f"{log_level['info']} Applying config file")
    devices = {}
    for device in config["autofat"]["network"]:
        devices[device["name"]] = {"ip": device["ip"], "user": device["credentials"]["user"], "pwd": device["credentials"]["pwd"]}

    # console.log(devices)
    
    console.log(f"{log_level['info']} Searching for FATs")

    # access FAT dir, add all yaml-files and insert into status
    status = []
    fatDir = get_abs_path("FATs")
    files = filetypeindir(fatDir, ".yaml")
    for file in files:
        file = get_abs_path(f"FATs/{file}")
        console.log(f"{log_level['info']} Found FAT: {file}")

        fat = read_yaml(file)
        
        # fat is empty or TODO: dont pass validation
        if not fat:
            console.log(f"{log_level['warning']} FAT {file} is invalid")
        else:
            status.append({"name": fat["name"],
                        "status": fat_status["pending"], 
                        "file": file, 
                        "content": fat})
    
    # console.log(status)

    console.log(f"{log_level['info']} Ordering FATs")
    
    # sort FATs by priority
    x = 0
    while x < (len(status) - 1):
        y = len(status) - 1

        while y > x:
            pri_x = [status[x]["content"]["priority"] if "priority" in status[x]["content"] else 0]
            pri_y = [status[y]["content"]["priority"] if "priority" in status[y]["content"] else 0]

            if pri_y > pri_x:
                temp = status[x]
                status[x] = status[y]
                status[y] = temp
            
            y -= 1
        x += 1
        

    # ------------------------------------------------------
    # Loop and do FATs
    # ------------------------------------------------------
        
    for fat in status:
        console.log(f"\n{log_level['info']} Beginning FAT: {fat['name']}")
        fat["status"] = fat_status["running"]

        for task in fat["content"]["tasks"]:
            console.log(f"{log_level['info']} Doing task: {task['name']}")

            # if task expect is of type boolean
            if task["expect"]["type"] == "boolean":
                if task["device"] == "laptop":
                    result = run_bool(task["command"])
                else:
                    result = run_bool(task["command"], devices[task["device"]])
                
                if result == task["expect"]["value"]:
                    console.log(f"{log_level['info']} Task successfully completed")
                else:
                    fat["status"] = fat_status["failed"]
                    console.log(f"{log_level['error']} Task failed")
                    break
            
            # if task expect is of type manual
            elif task["expect"]["type"] == "manual":
                userInput = "R"
                while userInput == "R" or userInput == "REPEAT":
                    console.print(f"\t\t[bright_yellow]    {task['expect']['prompt']}[/bright_yellow]", end=" ")

                    if task["device"] == "laptop":
                        _ = run_bool(task["command"])
                    else:
                        _ = run_bool(task["command"], devices[task["device"]])

                    userInput = input("(y/N, r = repeat): ").upper()
                    
                    if userInput == "Y" or userInput == "YES":
                        taskValue = True
                    elif userInput == "R" or userInput == "REPEAT":
                        continue
                    else:
                        taskValue = False

                    if taskValue == task["expect"]["value"]:
                        console.log(f"{log_level['info']} Task: {task['name']} was successfully completed")
                    else:
                        console.log(f"{log_level['warning']} Task: {task['name']} was not completed")
                        fat["status"] = fat_status["failed"]
                        break
                if fat["status"] == fat_status["failed"]:
                    break
                
        # check fat status 
        if fat["status"] == fat_status["running"]:
            fat["status"] = fat_status["success"]    
        elif fat["status"] == fat_status["failed"] and "priority" in fat["content"]:
            break


    # ------------------------------------------------------
    # End
    # ------------------------------------------------------    

    console.rule("Summary")

    table = Table(box=box.MINIMAL)

    table.add_column("File", justify="left")
    table.add_column("FAT", justify="left", min_width=20)
    table.add_column("Status", justify="right")

    for row in status:  
        table.add_row(row["file"], row["name"], row["status"])

    console.print(table)




if __name__ == "__main__":
    fire.Fire(main)