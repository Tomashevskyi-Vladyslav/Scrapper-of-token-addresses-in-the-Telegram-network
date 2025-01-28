import os
import time
import psutil
import subprocess

def is_program_running(script_name):
    """
    Checks if a Python script is running.
    :param script_name: The name of the script to check (e.g., 'Untitled.py').
    :return: True if running, False otherwise.
    """
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):

        try:
            cmdline = proc.info['cmdline']  # Get the cmdline of the process

            if cmdline and script_name in cmdline:  # Ensure cmdline is not None
                return True
            
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False

def restart_program(script_path):
    """
    Restarts a Python script using subprocess.
    :param script_path: The path to the script (e.g., 'Untitled.py').
    """
    print(f"Starting {script_path}...")
    subprocess.Popen(['python', script_path])

def monitor_script(script_name, script_path):
    """
    Continuously monitors the script and restarts it if not running.
    :param script_name: The name of the script (e.g., 'Untitled.py').
    :param script_path: The path to the script (e.g., 'Untitled.py').
    """
    while True:

        if not is_program_running(script_name):
            restart_program(script_path)

        time.sleep(5)  # Check every 5 seconds

# Monitor 'Untitled.py'
monitor_script('Untitled.py', 'Untitled.py')