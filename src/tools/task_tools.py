from src.tools.rich_print import log_level, fat_status
from src.tools.cli_tools import run_bool, run_str, run_presistent

from rich.console import Console


def run_task(fat: dict | list, task: dict | list, console: Console) -> bool:
    # if a task fail
    def task_fail(fat: dict | list, command: str):
        fat["status"] = fat_status["failed"]
        console.log(f"{log_level['error']} [red]Failed at running command:[/red] {command}")

    # if task expect is of type boolean
    if task["expect"]["type"] == "boolean":
        result = run_bool(task["command"])
        
        if result == task["expect"]["value"]:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False

    # if task expect is of type string
    elif task["expect"]["type"] == "string":
        result = run_str(task["command"])
        
        if isinstance(task["expect"]["value"], str) and task["expect"]["value"] in result:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        elif isinstance(task["expect"]["value"], list) and all(item in result for item in task["expect"]["value"]):
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False

    # if task expect is of type int
    elif task["expect"]["type"] == "int":
        result = int(run_str(task["command"]))

        if "value" in task["expect"] and result == task["expect"]["value"]:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        elif result in range(task["expect"]["minvalue"], task["expect"]["maxvalue"]): # assume result in a range 
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False


    # if task expect is of type array
    elif task["expect"]["type"] == "array":
        result = run_str(task["command"])
        
        if str(task["expect"]["value"]) in result:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False

    # if task expect is of type manual
    elif task["expect"]["type"] == "manual":
        userInput = "R"
        while userInput == "R" or userInput == "REPEAT":
            console.print(f"\t\t[bright_yellow]    {task['expect']['prompt']}[/bright_yellow]", end=" ")

            if "command" in task:
                _ = run_bool(task["command"])

            userInput = input("(y/N, r = repeat): ").upper()
            
            if userInput == "Y" or userInput == "YES":
                taskValue = True
            elif userInput == "R" or userInput == "REPEAT":
                continue
            else:
                taskValue = False

            if taskValue == task["expect"]["value"]:
                console.log(f"{log_level['info']} Task successfully completed"); return True
            else:
                task_fail(fat, task["command"]); return False
            
        if fat["status"] == fat_status["failed"]:
            return False
    
    elif task["expect"]["type"] == "persistent":
        result = run_presistent(task["command"])
        
        if result == task["expect"]["value"]:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False