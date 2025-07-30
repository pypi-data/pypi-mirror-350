import yaml

# Définir la classe Paramètre
class Params:
    def __init__(self, path):
        config = self._initParams(path)  # Appel correct de la méthode

        self.general = config.get('general', {})
        self.acoustic = config.get('acoustic', {})
        self.optic = config.get('optic', {})

    def __repr__(self):
        return (f"Params(general={self.general}, acoustic={self.acoustic}, optic={self.optic})")

    def _initParams(self, path):
        """
        Initialize parameters from the YAML configuration file.
        """
        if not path.endswith('.yaml'):
            raise ValueError("The configuration file must be a YAML file with a .yaml extension.")

        try:
            with open(path, 'r') as file:
                config = yaml.safe_load(file)
                if config is None:
                    raise ValueError("The configuration file is empty or not valid YAML.")

                # Vérifiez si 'Parameters' est la clé racine
                if 'Parameters' in config:
                    config = config['Parameters']

                print("Configuration loaded:", config)
                return config  # Retourne le dictionnaire config
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {path} does not exist.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

