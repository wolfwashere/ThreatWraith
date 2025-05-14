import platform
import subprocess
import os
from colorama import Fore, Style

# Tracks artifacts for ghost mode cleanup
ghost_cleanup_queue = {
    "files": [],
    "registry": []
}

def simulate_artifacts(step, ghost_mode=False, training_dir=None):
    artifacts = step.get('artifacts', [])
    if not artifacts:
        return

    current_os = platform.system().lower()

    for artifact in artifacts:
        artifact_type = artifact.get('type')

        # -------------------- FILE ARTIFACT --------------------
        if artifact_type == 'file':
            path = artifact.get('path', 'outputs/simulated_drop.txt')
            contents = artifact.get('contents', 'Simulated artifact content.')

            # Redirect file path if training mode is enabled
            if training_dir:
                basename = os.path.basename(path)
                path = os.path.join(training_dir, "dropped_files", basename)
                os.makedirs(os.path.dirname(path), exist_ok=True)

            try:
                with open(path, 'w') as f:
                    f.write(contents)
                print(f"{Fore.GREEN}    -> File dropped: {path}{Style.RESET_ALL}")
                if ghost_mode and path not in ghost_cleanup_queue["files"]:
                    ghost_cleanup_queue["files"].append(path)
            except:
                print(f"{Fore.RED}    -> Failed to write file: {path}{Style.RESET_ALL}")

        # -------------------- REGISTRY ARTIFACT --------------------
        elif artifact_type == 'registry' and 'windows' in current_os:
            key = artifact.get('key')
            value = artifact.get('value')
            cmd = f'reg add "{key}" /v {value} /t REG_SZ /d SimulatedEntry /f'
            try:
                subprocess.run(cmd, shell=True, check=True)
                print(f"{Fore.GREEN}    -> Registry key simulated: {key}\\{value}{Style.RESET_ALL}")
                if ghost_mode:
                    ghost_cleanup_queue["registry"].append((key, value))
            except:
                print(f"{Fore.RED}    -> Failed to simulate registry key.{Style.RESET_ALL}")

        # -------------------- EVENTLOG ARTIFACT --------------------
        elif artifact_type == 'eventlog' and 'windows' in current_os:
            source = artifact.get('source', 'ThreatWraith')
            message = artifact.get('message', 'Simulated event log')
            try:
                subprocess.run(
                    f'eventcreate /T INFORMATION /ID 100 /L APPLICATION /SO "{source}" /D "{message}"',
                    shell=True,
                    check=True
                )
                print(f"{Fore.GREEN}    -> Event log created: {message}{Style.RESET_ALL}")
                if ghost_mode:
                    subprocess.run('wevtutil cl Application', shell=True)
                    print(f"{Fore.YELLOW}    -> Event log cleared (ghost mode){Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}    -> Failed to create or clear event log.{Style.RESET_ALL}")

        # -------------------- NETWORK ARTIFACT --------------------
        elif artifact_type == 'network':
            host = artifact.get('host', 'example.com')
            port = artifact.get('port', 80)
            try:
                subprocess.run(f'nc -zv {host} {port}', shell=True, check=True)
                print(f"{Fore.GREEN}    -> Simulated connection to {host}:{port}{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}    -> Failed to simulate network traffic to {host}{Style.RESET_ALL}")

        else:
            print(f"{Fore.YELLOW}    -> Skipping unsupported artifact type: {artifact_type}{Style.RESET_ALL}")

    if ghost_mode:
        cleanup_ghost_artifacts()


# -------------------- GHOST MODE CLEANUP --------------------
def cleanup_ghost_artifacts():
    for path in ghost_cleanup_queue["files"]:
        try:
            os.remove(path)
            print(f"{Fore.BLUE}[GHOST] Deleted file: {path}{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[GHOST] Failed to delete file: {path}{Style.RESET_ALL}")

    for key, value in ghost_cleanup_queue["registry"]:
        try:
            subprocess.run(f'reg delete "{key}" /v {value} /f', shell=True, check=True)
            print(f"{Fore.BLUE}[GHOST] Deleted registry key: {key}\\{value}{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[GHOST] Failed to delete registry key: {key}\\{value}{Style.RESET_ALL}")

    ghost_cleanup_queue["files"].clear()
    ghost_cleanup_queue["registry"].clear()
