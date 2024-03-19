from src.tools.rich_print import log_level, fat_status
from src.tools.cli_tools import run_bool, run_str, run_persistent

from rich.console import Console


def run_task(fat: dict | list, task: dict | list, console: Console) -> bool:
    """
    Execute a task within a FAT, extracting data from a YAML file.

    Args:
        fat: The FAT this task is part of.
        task: Contains the task type, command, and expected value.
        console: An instance of the Console class used for logging and displaying messages.

    Returns:
        bool: True if the task succeeds, False otherwise.
    """
    # Function to handle task failure
    def task_fail(fat: dict | list, command: str):
        fat["status"] = fat_status["failed"]
        if "error" in task and task["error"] is not None:
            console.log(f"{log_level['error']} [red]{task["error"]}[/red]")
        console.log(f"{log_level['error']} [red]Failed at running command:[/red] {command}")

    # If the expected result of the task is of type boolean
    if task["expect"]["type"] == "boolean":
        result = run_bool(task["command"])
        
        if result == task["expect"]["value"]:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False

    # If the expected result of the task is of type string
    elif task["expect"]["type"] == "string":
        result = run_str(task["command"])
        
        if isinstance(task["expect"]["value"], str) and task["expect"]["value"] in result:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        elif isinstance(task["expect"]["value"], list) and all(item in result for item in task["expect"]["value"]):
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False

    # If the expected result of the task is of type int
    elif task["expect"]["type"] == "int":
        result = int(run_str(task["command"]))

        if "value" in task["expect"] and result == task["expect"]["value"]:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        # If the expected result is within a range of int values
        elif result in range(task["expect"]["minvalue"], task["expect"]["maxvalue"]): 
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False

    # If the expected result of the task is of type array
    elif task["expect"]["type"] == "array":
        result = run_str(task["command"])
        
        if str(task["expect"]["value"]) in result:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        else:
            task_fail(fat, task["command"]); return False

    # If the task requires manual verification
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

    # If the task has a persistent expectation
    elif task["expect"]["type"] == "persistent":
        result, perString = run_persistent(task["command"], task["expect"]["string"])
        
        if result == task["expect"]["value"] and task["expect"]["string"] in perString:
            console.log(f"{log_level['info']} Task successfully completed"); return True
        elif task["expect"]["string"] not in perString:
            console.log(f"{log_level['warning']} [bright_yellow]Could not find expected string:[/bright_yellow] {task["expect"]["string"]}")
            task_fail(fat, task["command"]); return False
        else:
            task_fail(fat, task["command"]); return False
