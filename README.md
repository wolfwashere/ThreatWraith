# ThreatWraith
**Adversary Simulation and Detection Training Framework**

ThreatWraith is a modular red team simulator designed to generate realistic attack behavior for blue team detection training. Inspired by frameworks like Atomic Red Team and Darktrace, ThreatWraith lets you execute scenario playbooks that simulate real-world intrusions across multiple MITRE ATT&CK stages.

## 🔥 Features
- Modular YAML-defined attack scenarios
- File, registry, PowerShell, and network artifact generation
- MITRE ATT&CK tagging for each action
- Detection timeline and reporting engine
- Ghost mode: ephemeral simulations with rollback
- Optional web dashboard (Flask-based)

## 🧠 Use Cases
- Blue team training and detection tuning
- Forensics and IR practice
- Adversary behavior simulation for threat modeling

## 📦 Example Scenario (YAML)
```yaml
- id: T1059.001
  name: PowerShell Reverse Shell
  command: powershell -enc <base64>
  sleep: 5-10
  tags: [execution, C2]
