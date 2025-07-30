# fbcli/config.py

import os
import runpy
from pathlib import Path

CONFIG_ENV_VAR = "FBCLI_CONFIG_PATH"
CONFIG_DIR = Path.home() / ".fbcli"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "config.fb"
SAVED_PATH_FILE = CONFIG_DIR / "config_path.txt"

def prompt_for_config_path():
    print("📁 fbcli config file not found.")
    user_path = input("Enter path to your config.fb (or press Enter to create default at ~/.fbcli/config.fb): ").strip()

    if user_path:
        # Handle quotes from Windows "Copy as path"
        cleaned_path = Path(user_path.strip('"')).expanduser()
        if not cleaned_path.exists():
            print(f"❌ File does not exist: {cleaned_path}")
            raise FileNotFoundError(f"Invalid config path: {cleaned_path}")

        # Save for future runs
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        SAVED_PATH_FILE.write_text(str(cleaned_path))
        print(f"✅ Using and saving config path: {cleaned_path}")
        return cleaned_path
    else:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not DEFAULT_CONFIG_PATH.exists():
            DEFAULT_CONFIG_PATH.write_text("# Example fbcli config\nservers = {}\n")
            print(f"✅ Created default config at: {DEFAULT_CONFIG_PATH}")
        SAVED_PATH_FILE.write_text(str(DEFAULT_CONFIG_PATH))
        return DEFAULT_CONFIG_PATH

# Step 1: Check env override
if CONFIG_ENV_VAR in os.environ:
    config_path = Path(os.environ[CONFIG_ENV_VAR].strip('"')).expanduser()

# Step 2: Check saved path
elif SAVED_PATH_FILE.exists():
    config_path = Path(SAVED_PATH_FILE.read_text().strip()).expanduser()

# Step 3: Prompt user
elif DEFAULT_CONFIG_PATH.exists():
    config_path = DEFAULT_CONFIG_PATH
else:
    config_path = prompt_for_config_path()

# Load config
try:
    config = runpy.run_path(str(config_path))
    servers = config.get("servers", {})
except Exception as e:
    raise RuntimeError(f"Failed to load config from {config_path}:\n{e}")
