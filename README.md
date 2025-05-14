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
  os: windows
  sleep: 3-6
  tags: [execution, C2]
  artifacts:
    - type: file
      path: C:\Users\Public\ghost.exe
      contents: reverse shell placeholder
```

## 🚀 Quickstart  
```bash
git clone https://github.com/wolfwashere/ThreatWraith.git
cd ThreatWraith
pip install -r requirements.txt
```

Run a scenario:  
```bash
python3 main.py --scenario scenarios/sample_infection.yml
```

Ghost Mode (auto cleanup):  
```bash
python3 main.py --scenario scenarios/sample_infection.yml --ghost
```

Training Case Output:  
```bash
python3 main.py --scenario scenarios/sample_infection.yml --train
```

## 🌐 Web UI  
```bash
python3 webui/app.py
```

Access at:  
```
http://127.0.0.1:5000
```

Features:
- Build and edit scenarios
- Launch attack playbooks
- View execution logs and tags

## 🗂️ Training Case Output Structure  
```
outputs/training_cases/YYYY-MM-DD_HHMMSS/
├── scenario.yml
├── run_log.txt
├── run_log.json
├── README.txt
├── dropped_files/
└── YYYY-MM-DD_HHMMSS.zip
```

## 🛠 Roadmap  
- [ ] MITRE tactic-based filtering  
- [ ] Scenario scoring system for defenders  
- [ ] Randomized adversary profiles  
- [ ] WebSocket-powered live output feed  
- [ ] Training case replay from ZIP  

## 📄 License  
MIT License. Use responsibly and only in authorized environments.

## 🧑‍💻 Author  
[@wolfwashere](https://github.com/wolfwashere) — built for real-world detection, adversary simulation, and incident response training.

