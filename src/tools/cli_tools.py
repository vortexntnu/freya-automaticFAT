#!/usr/bin/env python

import subprocess

# run command, output true/false => command success or not
def run_bool(command: str, device: object = None) -> bool:
    if device:
        command = ssh_wrap(command, device)

    result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Check the command's return code (0 means success)
    return result.returncode == 0

# run command, output text
def run_str(command: str, device: object = None) -> str:
    if device:
        command = ssh_wrap(command, device)

    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    return result.decode("utf-8")


# add ssh wrapping to command
def ssh_wrap(command: str, device: dict) -> str:
    ip = device["ip"]
    user = device["user"]
    pwd = device["pwd"]

    new_command = 'sshpass -p "{}" ssh {}@{} "{}"'.format(pwd, user, ip, command)

    return new_command

