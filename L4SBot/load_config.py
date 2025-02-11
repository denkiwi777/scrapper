import yaml

def load_config(file):
    with open(file, encoding='utf-8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)