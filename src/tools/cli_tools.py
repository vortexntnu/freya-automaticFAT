#!/usr/bin/env python

import subprocess
from typing import Union

# run command, output true/false => command success or not
def run_bool(command: str) -> bool:
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        return result.returncode == 0
    
    except Exception as e:
        return False

# run command, output text
def run_str(command: str) -> str:
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        
        return result.decode("utf-8")

    except Exception as e:
        print("Command failed, check if needed package is installed.")
        return ""


# add ssh wrapping to command
def ssh_wrap(command: str, device: dict) -> str:
    ip = device["ip"]
    user = device["user"]
    pwd = device["pwd"]

    new_command = 'sshpass -p "{}" ssh {}@{} "{}"'.format(pwd, user, ip, command)

    return new_command

