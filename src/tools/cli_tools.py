#!/usr/bin/env python

import subprocess
import time
import atexit

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

def run_presistent(command: str) -> bool:
    try:
        process = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT)

        # await process start
        while process.poll() is None:
            time.sleep(1)

        # clean up process at exit
        def cleanup() -> None:
            process.terminate()
            process.wait()
        atexit.register(cleanup())
        
        return True
    
    except Exception as e:
        return False


# add ssh wrapping to command
def ssh_wrap(command: str, device: dict) -> str:
    ip = device["ip"]
    user = device["user"]
    pwd = device["pwd"]

    new_command = 'sshpass -p "{}" ssh {}@{} "{}"'.format(pwd, user, ip, command)

    return new_command

