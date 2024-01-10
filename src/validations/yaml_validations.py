from src.tools.rich_print import log_level

from rich.console import Console

types = ["boolean", "manual", "string", "int", "array"]

# the validator of yamles
def config_yamVal(data: dict | list, console: Console) -> bool:
    # Validate root attributes
    if "autofat" not in data:
        console.log(f"{log_level['error']} Config lacks root: 'autofat'.")
        return False
    else:
        autofat_data = data["autofat"]

        if "network" not in autofat_data:
            console.log(f"{log_level['error']} Config lacks 'network' property under root 'autofat'.")
            return False

    # Network validation
    for node in autofat_data.get("network", []):
        name = node.get("name")

        if "name" not in node:
            console.log(f"{log_level['error']} Network segment lacks 'name'.")
            return False

        if "ip" not in node:
            console.log(f"{log_level['error']} Network segment '{name}' lacks 'ip' configuration.")
            return False

        credentials = node.get("credentials")

        if not credentials:
            console.log(f"{log_level['error']} Network segment '{name}' lacks 'credentials' configuration.")
            return False
        else:
            if "user" not in credentials:
                console.log(f"{log_level['error']} Credentials segment for '{name}' lacks 'user'.")
                return False
            if "pwd" not in credentials:
                console.log(f"{log_level['error']} Credentials segment for '{name}' lacks 'password'.")
                return False
            
    return True

def fat_yamVal(data: dict | list, devices: dict, console: Console) -> bool:
    if not data:
        console.log(f"{log_level['warning']} FAT is empty.")
        return False

    if "name" not in data:
        console.log(f"{log_level['warning']} FAT lacks a name.")
        return False

    if "tasks" not in data:
        console.log(f"{log_level['warning']} FAT: {data['name']}, lacks tasks.")
        return False
    
    for task in data["tasks"]:
        if "name" not in task or task["name"] == None:
            console.log(f"{log_level['warning']} FAT: {data['name']}, Task lacks a name.")
            return False
        
        if "device" in task:
            if not task["device"] == "laptop":
                if not task["device"] in devices:
                    console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, device in task does not match any stated in config ({devices}).")
                    return False

        if "expect" not in task or task["expect"] == None:
            console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, lacks an expect.")
            return False
        
        if not type(task["expect"]) is list and not type(task["expect"]) is dict:
            console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, expect is misconfigured.")
            return False
        
        if "type" not in task["expect"] or task["expect"]["type"] == None:
            console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, in lacks a expect type.")
            return False
        
        if not task["expect"]["type"] in types:
            console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, expect type is an unsupported type, must be either manual, boolean, string, int or array.")
            return False

        if task["expect"]["type"] == "int":
            if "minvalue" in task["expect"]:
                if "maxvalue" not in task["expect"] or task["expect"]["maxvalue"] == None:
                    console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, lacks a expect value.")
                    return False
            if "maxvalue" in task["expect"]:
                if "minvalue" not in task["expect"] or task["expect"]["minvalue"] == None:
                    console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, lacks a expect value.")
                    return False
        elif "value" not in task["expect"] or task["expect"]["value"] == None:
            console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, lacks a expect value.")
            return False
        
        if task["expect"]["type"] == "boolean":
            if not task["expect"]["value"] == True and not task["expect"]["value"] == False:
                console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, expect value is an unsupported value, must be eather True or False.")
                return False
        
        if task["expect"]["type"] == "manual":
            if "prompt" not in task["expect"] or task["expect"]["prompt"] == None:
                console.log(f"{log_level['warning']} FAT: {data['name']}, Task: {task['name']}, a manual expect needs a prompt (question to be answered).")
                return False
        elif task["expect"]["type"] == "boolean":
            if "command" not in task or task["command"] == None:
                console.log(f"{log_level['warning']} FAT: {data['name']}, Task {task['name']}, a boolean expect needs a task command.")
                return False

    return True
