import json
import os
from datetime import datetime

# Default output paths
DEFAULT_TXT_PATH = "outputs/run_log.txt"
DEFAULT_JSON_PATH = "outputs/run_log.json"

def log_action(step, success=True, output_path=None):
    status = "success" if success else "fail"
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Resolve log file paths
    if output_path:
        txt_path = os.path.join(output_path, "run_log.txt")
        json_path = os.path.join(output_path, "run_log.json")
    else:
        txt_path = DEFAULT_TXT_PATH
        json_path = DEFAULT_JSON_PATH

    # Text log (human-readable)
    with open(txt_path, "a") as f:
        f.write(f"[{timestamp}] [{status.upper()}] {step.get('id')} - {step.get('name')}\n")

    # Structured JSON log (for UI/timeline)
    json_entry = {
        "id": step.get("id", "N/A"),
        "name": step.get("name", ""),
        "command": step.get("command", ""),
        "tags": step.get("tags", []),
        "sleep": step.get("sleep", "0"),
        "status": status,
        "timestamp": timestamp
    }

    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            log_data = json.load(f)
    else:
        log_data = []

    log_data.append(json_entry)

    with open(json_path, "w") as f:
        json.dump(log_data, f, indent=2)
