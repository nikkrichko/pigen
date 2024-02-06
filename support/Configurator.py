import yaml

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = cls._load_config()
        return cls._instance

    @staticmethod
    def _load_config():
        try:
            with open('config.yaml', 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError("config.yaml not found in the current directory.")

    def get(self, key):
        if key in self._config:
            return self._config[key]
        else:
            raise KeyError(f"'{key}' not found in the configuration.")
