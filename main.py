import argparse
import os
import shutil
from datetime import datetime
from utils.config import load_scenario
from engine.executor import execute_step
from colorama import Fore, Style

def main():
    parser = argparse.ArgumentParser(description="Run a ThreatWraith scenario")
    parser.add_argument('--scenario', required=True, help='Path to scenario YAML')
    parser.add_argument('--dry-run', action='store_true', help='Preview actions without executing')
    parser.add_argument('--ghost', action='store_true', help='Enable Ghost Mode (auto-cleanup)')
    parser.add_argument('--train', action='store_true', help='Enable training case output mode')
    args = parser.parse_args()

    scenario_path = args.scenario
    scenario = load_scenario(scenario_path)

    # Prepare training output folder if needed
    training_dir = None
    if args.train:
        case_id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        training_dir = f"outputs/training_cases/{case_id}"
        os.makedirs(training_dir, exist_ok=True)

        # Copy the scenario into the training folder
        shutil.copy(scenario_path, os.path.join(training_dir, "scenario.yml"))

        # Write README.txt as challenge context
        with open(os.path.join(training_dir, "README.txt"), "w") as f:
            f.write(f"""ThreatWraith Training Case: {case_id}

Scenario: {os.path.basename(scenario_path)}
Date Generated: {datetime.now().isoformat()}

Instructions:
- Analyze logs and artifacts in this folder
- Try to answer:
  • What was the initial attack vector?
  • Was persistence established? How?
  • What file or registry key should be removed?
  • What would you alert on?

Happy hunting.
""")

    # Clean run_log.json if not in training mode
    if not args.train:
        if os.path.exists("outputs/run_log.json"):
            os.remove("outputs/run_log.json")

    # Execute each step in scenario
    for step in scenario:
        execute_step(
            step,
            dry_run=args.dry_run,
            ghost_mode=args.ghost,
            train_dir=training_dir
        )

    # Auto-zip the training case folder (if in training mode)
    if training_dir:
        zip_path = f"{training_dir}.zip"
        shutil.make_archive(training_dir, 'zip', training_dir)
        print(f"{Fore.CYAN}[✓] Training case archived to: {zip_path}{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
