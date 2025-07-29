import sys
import threading
import queue
import re
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from termcolor import cprint
from .utils import load_config, get_random_user_agent, setup_logger

BSB_LOGO = r"""
┳┓┏┓┳┓
┣┫┗┓┣┫
┻┛┗┛┻┛
      """

# সাধারণ SQL Error Patterns (MySQL, MSSQL, PostgreSQL)
ERROR_PATTERNS = [
    r"SQL syntax.*MySQL",
    r"Warning.*mysql_",
    r"Unclosed quotation mark after the character string",
    r"quoted string not properly terminated",
    r"SQLSTATE\w+",
    r"PG::SyntaxError",
    r"System\.Data\.SqlClient\.SqlException"
]

class SQLTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.parsed = urlparse(base_url)
        self.qs = parse_qs(self.parsed.query)
        self.logger = setup_logger('check_sql')
        cfg = load_config()
        self.timeout = cfg.get('DEFAULT_TIMEOUT', 10)
        self.thread_count = cfg.get('THREAD_COUNT', 10)
        self.payloads = cfg.get('SQLI_PAYLOADS', [])
        self.headers = {'User-Agent': get_random_user_agent()}
        self.vulnerable_params = []
        self.results = queue.Queue()

    def is_error_in_response(self, response_text):
        for pat in ERROR_PATTERNS:
            if re.search(pat, response_text, re.IGNORECASE):
                return True
        return False

    def test_param(self, param):
        original_resp = requests.get(self.base_url, headers=self.headers, timeout=self.timeout)
        original_length = len(original_resp.text)
        for payload in self.payloads:
            new_qs = self.qs.copy()
            new_qs[param] = payload
            new_query = urlencode(new_qs, doseq=True)
            new_url = urlunparse((
                self.parsed.scheme, self.parsed.netloc, self.parsed.path,
                self.parsed.params, new_query, self.parsed.fragment
            ))
            try:
                test_resp = requests.get(new_url, headers=self.headers, timeout=self.timeout)
                self.logger.info(f"Param: {param} | Payload: {payload} | Status: {test_resp.status_code}")
                if self.is_error_in_response(test_resp.text) or abs(len(test_resp.text) - original_length) > 50:
                    self.results.put((param, payload, new_url))
                    return
            except Exception as e:
                self.logger.error(f"Error testing {new_url}: {e}")
        # যদি vulnerability না মেলে:
        self.results.put((param, None, None))

    def run(self):
        if not self.qs:
            cprint(BSB_LOGO, "cyan")
            cprint("[BSB] No query parameters found to test.", "yellow")
            return

        cprint(BSB_LOGO, "cyan")
        cprint(f"[BSB] Starting multithreaded SQL Injection tests on: {self.base_url}", "green")

        threads = []
        for param in self.qs:
            t = threading.Thread(target=self.test_param, args=(param,))
            t.daemon = True
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.summarize_results()

    def summarize_results(self):
        vulnerable_found = False
        while not self.results.empty():
            param, payload, url = self.results.get()
            if payload:
                cprint(f"[BSB] Parameter '{param}' IS VULNERABLE with payload: {payload}", "red")
                cprint(f"[BSB] Exploitable URL: {url}", "red")
                vulnerable_found = True
                self.logger.warning(f"VULNERABLE -> Param: {param} Payload: {payload} URL: {url}")
            else:
                cprint(f"[BSB] Parameter '{param}' appears NOT vulnerable.", "blue")
                self.logger.info(f"NOT VULNERABLE -> Param: {param}")

        if not vulnerable_found:
            cprint("[BSB] No vulnerability detected in tested parameters.", "blue")

def main():
    if len(sys.argv) != 2:
        cprint("Usage: black-c <url_with_params>", "yellow")
        return
    tester = SQLTester(sys.argv[1])
    tester.run()
