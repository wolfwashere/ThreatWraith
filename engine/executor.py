import subprocess
import time
import random
import platform
import os
from colorama import Fore, Style
from utils.logger import log_action
from engine.artifact_sim import simulate_artifacts

def execute_step(step, dry_run=False, ghost_mode=False, train_dir=None):
    cmd = step['command']
    target_os = step.get('os', 'any').lower()
    current_os = platform.system().lower()

    if target_os != 'any' and target_os not in current_os:
        print(f"{Fore.YELLOW}[!] Skipping step '{step['name']}' (requires {target_os}, current OS is {current_os}){Style.RESET_ALL}")
        log_action(step, success=False, output_path=train_dir)
        return

    # Sleep time logic
    sleep_range = step.get('sleep', 0)
    if isinstance(sleep_range, int):
        sleep_time = sleep_range
    elif isinstance(sleep_range, str) and '-' in sleep_range:
        try:
            low, high = map(int, sleep_range.split('-'))
            sleep_time = random.randint(low, high)
        except:
            sleep_time = 0
    else:
        sleep_time = 0

    print(f"{Fore.CYAN}[+] Executing: {step['name']} ({step['id']}){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}    -> Command: {cmd}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}    -> Sleeping for {sleep_time} seconds...{Style.RESET_ALL}")

    if not dry_run:
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"{Fore.GREEN}    -> Command executed successfully.{Style.RESET_ALL}")
            log_action(step, success=True, output_path=train_dir)
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}[!] Command failed: {e}{Style.RESET_ALL}")
            log_action(step, success=False, output_path=train_dir)
    else:
        print(f"{Fore.BLUE}[DRY RUN] Skipping actual execution.{Style.RESET_ALL}")
        log_action(step, success=True, output_path=train_dir)

    # Simulate forensic artifacts (logs, registry, file, etc.)
    simulate_artifacts(step, ghost_mode=ghost_mode, training_dir=train_dir)

    time.sleep(sleep_time)
