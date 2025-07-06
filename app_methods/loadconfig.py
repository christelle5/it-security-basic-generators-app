import json


class LoadConfig:
    @staticmethod
    def load_configuration(file_name, config_type) -> dict:
        pseudorandom_default_config = {
            "modulus": 2097151,
            "multiplier": 512,
            "increment": 144,
            "initial_value": 3
        }
        rc5_default_config = {
            "w": 64,
            "r": 20,
            "b": 16
        }
        config_file = file_name
        try:
            with open(config_file, "r") as file:
                configuration = json.load(file)
                return {"configuration": configuration, "error": None}
        except FileNotFoundError:
            if config_type == "pseudorandom":
                return {"configuration": pseudorandom_default_config,
                    "error": "Configuration file not found. Default parameters will be used."}
            if config_type == "rc5":
                return {"configuration": rc5_default_config,
                        "error": "Configuration file not found. Default parameters will be used."}
        except json.JSONDecodeError:
            # Помилка декодування JSON
            if config_type == "pseudorandom":
                return {"configuration": pseudorandom_default_config,
                    "error": "Error decoding the configuration file."}
            if config_type == "rc5":
                return {"configuration": rc5_default_config,
                    "error": "Error decoding the configuration file."}

