import json
from os import getcwd, path

class Config():
    def get(self, module_name: str, key: str = None):
        config_path = path.join(getcwd(), 'config.json')
        keys = module_name.split('.')
        keys.extend(key.split('.')) if key else None
        with open(config_path, encoding='utf-8') as file:
            value = json.load(file)
            for k in keys:
                value = value[k]
            return value

def getConfig() -> Config:
    return Config()