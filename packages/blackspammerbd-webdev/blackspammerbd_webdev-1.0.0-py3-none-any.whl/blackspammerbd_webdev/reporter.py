from datetime import datetime
from typing import Any, Dict, List

from .utils import save_output
from .logger import logger

class Reporter:
    """
    Aggregates findings from all modules—links, SQL vulnerabilities, admin pages, brute-force—
    and writes a unified report to OUTPUT_DIR/report_<domain>_<timestamp>.<format>.
    """

    def __init__(self, domain: str) -> None:
        self.domain: str = domain.replace(":", "_")
        self.report: Dict[str, Any] = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "links": [],
            "sql_vulnerabilities": [],
            "admin_pages": [],
            "brute_force": []
        }

    def add_links(self, links: List[str]) -> None:
        self.report["links"] = links

    def add_sql_vuln(self, vuln_list: List[tuple]) -> None:
        # Each tuple: (payload, url)
        self.report["sql_vulnerabilities"] = [
            {"payload": payload, "url": url} for payload, url in vuln_list
        ]

    def add_admin_pages(self, pages: List[str]) -> None:
        self.report["admin_pages"] = pages

    def add_brute_results(self, results: Dict[str, str]) -> None:
        # If results dict is empty, store empty list
        if results:
            self.report["brute_force"] = [results]
        else:
            self.report["brute_force"] = []

    def generate(self) -> None:
        """
        Save the unified report to disk.
        """
        filename = f"report_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        save_output(self.domain, filename, self.report)
        logger.info(f"📄 Report generated: {filename}.{self.report.get('format', 'json')}")
