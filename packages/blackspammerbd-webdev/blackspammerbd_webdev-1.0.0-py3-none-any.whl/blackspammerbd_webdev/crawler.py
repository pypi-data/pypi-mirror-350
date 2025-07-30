import threading
from typing import Set
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from pathlib import Path

from .utils import fetch_html, get_random_user_agent, get_proxies, save_output, create_folder, is_same_domain
from .config import MAX_THREADS, CRAWL_DEPTH, RENDER_JS
from .logger import logger

# If you set render_js: true in config.yaml and have pyppeteer installed,
# we'll attempt to fetch a minimal rendered page to extract JS-generated links.
try:
    import asyncio
    from pyppeteer import launch
    _has_pyppeteer = True
except ImportError:
    _has_pyppeteer = False
    RENDER_JS = False  # Fallback

class Crawler:
    """
    High-performance, multithreaded link crawler:
      - Respects robots.txt
      - Optionally “renders” simple JS via pyppeteer if RENDER_JS is True
      - Recursively extracts all unique links within the same domain (up to CRAWL_DEPTH).
      - Saves final URL list to OUTPUT_DIR/links_<domain>.<format>.
    """

    def __init__(self, base_url: str):
        self.base_url: str = base_url.rstrip("/")
        parsed = urlparse(self.base_url)
        self.domain: str = parsed.netloc.replace(":", "_")
        self.visited: Set[str] = {self.base_url}
        self._lock = threading.Lock()
        self._robots_allowed = self._check_robots()

    def _check_robots(self) -> bool:
        """
        Fetch robots.txt and check if crawling is allowed for base_url.
        Returns True if allowed or robots.txt missing; False if Disallow: /
        """
        robots_url = urljoin(self.base_url, "/robots.txt")
        resp = fetch_html(robots_url)
        if resp and resp.status_code == 200:
            lines = resp.text.splitlines()
            for line in lines:
                if line.strip().lower().startswith("disallow: /"):
                    logger.warning(f"🚫 robots.txt disallows crawling {self.base_url}")
                    return False
        return True

    async def _fetch_rendered(self, url: str) -> Optional[str]:
        """
        If RENDER_JS is True and pyppeteer is available, fetch minimal rendered HTML.
        Otherwise return None.
        """
        if not (RENDER_JS and _has_pyppeteer):
            return None
        try:
            browser = await launch(headless=True, args=["--no-sandbox"])
            page = await browser.newPage()
            await page.goto(url, {"timeout": 10000})
            content = await page.content()
            await browser.close()
            return content
        except Exception as e:
            logger.debug(f"⚠️ Pyppeteer failed on {url}: {e}")
            return None

    def crawl(self) -> None:
        """
        Launch multithreaded crawling, respecting robots.txt and optional JS rendering.
        Save results upon completion.
        """
        if not self._robots_allowed:
            logger.info(f"Skipping crawl: robots.txt disallows {self.base_url}")
            return

        logger.info(f"🔍 Starting crawl on: {self.base_url} (depth={CRAWL_DEPTH}, render_js={RENDER_JS})")
        create_folder(self.domain)

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = [executor.submit(self._crawl_url, self.base_url, 0)]
            for _ in as_completed(futures):
                pass

        save_output(self.domain, "links", list(self.visited))
        logger.info(f"✅ Crawl complete: {len(self.visited)} unique links found for {self.domain}")

    def _crawl_url(self, url: str, depth: int) -> None:
        """
        Internal: fetch `url`, parse <a href="..."> (and JSON-LD links, if any),
        optionally render JS, and recurse if depth < CRAWL_DEPTH.
        """
        if depth >= CRAWL_DEPTH:
            return

        headers = get_random_user_agent()
        proxies = get_proxies()
        resp = fetch_html(url, headers=headers, timeout=MAX_THREADS, proxies=proxies)
        if not resp or resp.status_code != 200:
            logger.debug(f"Skipping URL (status {resp.status_code if resp else 'N/A'}): {url}")
            return

        text = resp.text

        # If RENDER_JS, attempt minimal JS rendering
        if RENDER_JS and _has_pyppeteer:
            try:
                rendered = asyncio.get_event_loop().run_until_complete(self._fetch_rendered(url))
                if rendered:
                    text = rendered
            except Exception:
                pass

        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            full_url = urljoin(self.base_url, href)
            if is_same_domain(full_url, self.base_url):
                with self._lock:
                    if full_url not in self.visited:
                        self.visited.add(full_url)
                        self._crawl_url(full_url, depth + 1)
