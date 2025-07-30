import runpy
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.fb"
config = runpy.run_path(str(CONFIG_PATH))
servers = config.get("servers", {})
