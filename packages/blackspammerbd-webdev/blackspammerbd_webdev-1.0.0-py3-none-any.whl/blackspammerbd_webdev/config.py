import yaml
import os
from typing import Any, Dict

def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load and parse the YAML configuration file.
    Raises:
      - FileNotFoundError if config.yaml does not exist.
      - yaml.YAMLError if the YAML format is invalid.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()

MAX_THREADS: int = config.get("max_threads", 20)
TIMEOUT: int = config.get("timeout", 5)
USE_PROXIES: bool = config.get("use_proxies", False)
PROXIES: list = config.get("proxy_list", [])
OUTPUT_FORMAT: str = config.get("output", {}).get("format", "json")
OUTPUT_DIR: str = config.get("output", {}).get("directory", "output")
CRAWL_DEPTH: int = config.get("crawl_depth", 3)
RENDER_JS: bool = config.get("render_js", False)
PAYLOAD_MODE: str = config.get("payload_mode", "quick")

# Paths to external payload files
SQL_PAYLOADS_FILE: str = config.get("sql_payloads_file", "blackspammerbd_webdev/payloads/sql_payloads.txt")
ADMIN_PATHS_FILE: str = config.get("admin_paths_file", "blackspammerbd_webdev/payloads/admin_paths.txt")
PASSWORDS_FILE: str = config.get("passwords_file", "blackspammerbd_webdev/payloads/passwords.txt")
USERNAMES_FILE: str = config.get("usernames_file", "blackspammerbd_webdev/payloads/usernames.txt")
USER_AGENTS_FILE: str = config.get("user_agents_file", "blackspammerbd_webdev/payloads/user_agents.txt")
