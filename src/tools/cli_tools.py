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
        # print("Command failed, check if needed package is installed.")
        return ""

def run_persistent(command: str, expectedString: str) -> tuple[bool, str]:
    process = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    try:
        while process.poll() is None:
            output = process.stdout.read().decode()
            process.stdout.seek(0)  # Reset file pointer position
            if expectedString in output:
                process.terminate()
                process.wait()  # Wait for termination
                return True, output
            time.sleep(5)    
        # If process finished without finding expected string
        output = process.stdout.read().decode()
        return False, output
        
    except Exception as e:
        return False, ""
    finally:
        # Clean up process at exit
        process.terminate()
        process.wait()


# add ssh wrapping to command
def ssh_wrap(command: str, device: dict) -> str:
    ip = device["ip"]
    user = device["user"]
    pwd = device["pwd"]

    new_command = 'sshpass -p "{}" ssh {}@{} "{}"'.format(pwd, user, ip, command)

    return new_command

