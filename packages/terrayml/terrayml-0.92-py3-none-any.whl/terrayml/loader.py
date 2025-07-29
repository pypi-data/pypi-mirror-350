import os
import yaml
from dotenv import load_dotenv

def load_yaml(yaml_file):
    """Load and process the YAML configuration file with environment variables."""
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"Error: {yaml_file} not found.")
    
    with open(yaml_file, "r") as file:
        raw_config = yaml.safe_load(file)

    return raw_config

def load_env_file(env_name):
    """Load environment variables from the corresponding .env file and validate required variables."""
    env_file = f"{env_name}.env"
    
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"❌ Error: Environment file '{env_file}' not found.")

    required_vars = get_required_variables()
    
    with open(env_file, "r") as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

    missing_vars = [var for var in required_vars if os.getenv(var) is None]
    
    if missing_vars:
        raise ValueError(f"❌ Missing required environment variables: {', '.join(missing_vars)}. "
                         f"Ensure they are set in {env_file}.")

    print(f"✅ Loaded environment variables from '{env_file}' successfully.")

def get_required_variables():
    """Read required variables from .env.example file."""
    example_file = ".env.example"
    
    if not os.path.exists(example_file):
        raise FileNotFoundError(f"❌ Error: Missing '.env.example' file, which defines required environment variables.")

    required_vars = []
    
    with open(example_file, "r") as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                key = line.split("=")[0].strip()
                required_vars.append(key)

    return required_vars
