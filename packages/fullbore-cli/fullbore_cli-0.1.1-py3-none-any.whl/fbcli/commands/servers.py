# fbcli/commands/servers.py

import subprocess
from fbcli.config import servers
from geezer import log, warn

def list():
    if not servers:
        warn("No servers configured", "config")
        return

    for name, info in servers.items():
        user = info.get("user", "root")
        host = info.get("host", "unknown")
        log(f"{name}: {user}@{host}", "📡", "servers")

def ssh(server_name: str):
    server = servers.get(server_name)
    if not server:
        warn(f"Server '{server_name}' not found", "lookup")
        return

    user = server.get("user", "root")
    host = server.get("host")
    if not host:
        warn(f"No host defined for '{server_name}'", "config")
        return

    log(f"Connecting to {user}@{host}", "🛜", "ssh")

    try:
        subprocess.run(["ssh", f"{user}@{host}"], check=True)
    except subprocess.CalledProcessError as e:
        warn(f"SSH command failed with exit code {e.returncode}", "ssh")
    except Exception as e:
        warn(f"SSH failed: {e}", "ssh")
