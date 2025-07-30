import os
from typing import List, Tuple

from ..utils import load_lines_from_file
from ..config import (
    SQL_PAYLOADS_FILE,
    ADMIN_PATHS_FILE,
    PASSWORDS_FILE,
    USERNAMES_FILE,
    USER_AGENTS_FILE,
    PAYLOAD_MODE
)

def load_sql_payloads() -> List[str]:
    """
    Return a list of SQL payloads from SQL_PAYLOADS_FILE.
    If PAYLOAD_MODE == "quick", return first 200; else return all.
    """
    all_payloads = load_lines_from_file(SQL_PAYLOADS_FILE)
    if PAYLOAD_MODE.lower() == "quick":
        return all_payloads[:200]
    return all_payloads

def load_admin_paths() -> List[str]:
    """
    Return a list of admin paths from ADMIN_PATHS_FILE.
    If PAYLOAD_MODE == "quick", return first 200; else all.
    """
    all_paths = load_lines_from_file(ADMIN_PATHS_FILE)
    if PAYLOAD_MODE.lower() == "quick":
        return all_paths[:200]
    return all_paths

def load_passwords() -> List[str]:
    """
    Return a list of passwords from PASSWORDS_FILE.
    If PAYLOAD_MODE == "quick", return first 200; else all.
    """
    all_pwds = load_lines_from_file(PASSWORDS_FILE)
    if PAYLOAD_MODE.lower() == "quick":
        return all_pwds[:200]
    return all_pwds

def load_usernames() -> List[str]:
    """
    Return a list of usernames from USERNAMES_FILE.
    """
    return load_lines_from_file(USERNAMES_FILE)

def load_user_agents() -> List[str]:
    """
    Return a list of user agents from USER_AGENTS_FILE.
    """
    return load_lines_from_file(USER_AGENTS_FILE)
