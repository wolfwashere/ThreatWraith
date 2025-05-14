import yaml

def load_scenario(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)
