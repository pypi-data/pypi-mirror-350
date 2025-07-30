import os
import json
import csv
import random
import requests
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urlparse

from .config import (
    OUTPUT_FORMAT,
    OUTPUT_DIR,
    TIMEOUT,
    USE_PROXIES,
    PROXIES,
    USER_AGENTS_FILE
)
from .logger import logger

_session: Optional[requests.Session] = None

def get_session() -> requests.Session:
    """
    Return a singleton requests.Session configured with exponential backoff retry logic.
    """
    global _session
    if _session is None:
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        _session = session
    return _session  # type: ignore

def load_lines_from_file(path: str) -> List[str]:
    """
    Read lines from a text file, strip whitespace, ignore empty lines.
    """
    result: List[str] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                ln = line.strip()
                if ln:
                    result.append(ln)
    except Exception as e:
        logger.error(f"❌ Failed to load payloads from {path}: {e}")
    return result

def load_user_agents() -> List[str]:
    """
    Load custom User-Agent strings from USER_AGENTS_FILE if provided.
    Returns an empty list if file missing or not set.
    """
    return load_lines_from_file(USER_AGENTS_FILE) if USER_AGENTS_FILE else []

custom_uas: List[str] = load_user_agents()

def get_random_user_agent() -> Dict[str, str]:
    """
    Return a dict with a random User-Agent header.
    Combines custom UAs (if any) with built-in ones from payloads/user_agents.txt.
    """
    from .payloads.user_agents import user_agents as default_uas
    pool: List[str] = custom_uas + default_uas
    if not pool:
        return {"User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"}
    ua: str = random.choice(pool)
    return {"User-Agent": ua}

def get_proxies() -> Dict[str, str]:
    """
    If USE_PROXIES is True and PROXIES list exists, return a random proxy dict.
    Otherwise, return an empty dict.
    """
    if USE_PROXIES and PROXIES:
        proxy: str = random.choice(PROXIES)
        return {"http": proxy, "https": proxy}
    return {}

def save_output(domain: str, filename: str, data: Any) -> None:
    """
    Save `data` under OUTPUT_DIR/<filename>_<domain>.<format>.
    Supported formats:
      - JSON (pretty-printed)
      - CSV (if list of dicts; else fallback to TXT)
      - TXT (one item per line)
    """
    out_dir = Path(OUTPUT_DIR)
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)

    output_file = out_dir / f"{filename}_{domain}.{OUTPUT_FORMAT}"

    try:
        if OUTPUT_FORMAT == "json":
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif OUTPUT_FORMAT == "csv":
            if isinstance(data, list) and data and isinstance(data[0], dict):
                keys = list(data[0].keys())
                with output_file.open("w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)  # type: ignore
            else:
                with output_file.open("w", encoding="utf-8") as f:
                    for item in data if isinstance(data, list) else [data]:
                        f.write(f"{item}\n")
        else:  # TXT
            with output_file.open("w", encoding="utf-8") as f:
                for item in data if isinstance(data, list) else [data]:
                    f.write(f"{item}\n")

        logger.info(f"✅ Output saved: {output_file}")
    except Exception as ex:
        logger.error(f"❌ Failed to save output to {output_file}: {ex}")

def create_folder(domain: str) -> Path:
    """
    Create (if needed) and return path to OUTPUT_DIR/links_<domain>/.
    """
    folder = Path(OUTPUT_DIR) / f"links_{domain}"
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"📂 Created folder: {folder}")
    return folder

def fetch_html(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = TIMEOUT,
    proxies: Optional[Dict[str, str]] = None
) -> Optional[requests.Response]:
    """
    Perform a GET request via Session with retry/backoff, given headers, timeout, and proxies.
    Returns Response if successful, else None.
    """
    session = get_session()
    proxies = proxies or {}
    try:
        resp = session.get(url, headers=headers, timeout=timeout, proxies=proxies)
        return resp
    except requests.RequestException as e:
        logger.error(f"❌ HTTP GET error at {url}: {e}")
        return None

def fetch_json(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = TIMEOUT,
    proxies: Optional[Dict[str, str]] = None
) -> Optional[Dict[str, Any]]:
    """
    GET request expecting JSON. Returns parsed dict or None.
    """
    try:
        resp = fetch_html(url, headers=headers, timeout=timeout, proxies=proxies)
        if resp and resp.status_code == 200:
            return resp.json()
    except ValueError:
        logger.error(f"❌ Invalid JSON response at {url}")
    return None

def is_same_domain(link: str, base: str) -> bool:
    """
    Check if `link` belongs to the same domain (or subdomain) as `base`.
    """
    return urlparse(link).netloc.endswith(urlparse(base).netloc)
