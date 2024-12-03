import json

# Default configuration for models and APIs
default_config = {
    "models": {
        "qwen2.5:0.5b": {
            "description": "Default physics book writer model",
            "system": """You are a Physics book Writer,
                         given a topic you will write a planned book.""",
            "num_ctx": 100000
        }
    },
    "apis": {
        "default_api": {
            "url": "http://localhost:11434",
            "description": "Local API for model generation"
        }
    }
}

# Save the default configuration to a JSON file
config_file_path = "config.json"
with open(config_file_path, "w") as config_file:
    json.dump(default_config, config_file, indent=4)




