import sys
import threading
import queue
import requests
from urllib.parse import urljoin, urlparse
from termcolor import cprint
from tqdm import tqdm
from .utils import load_config, get_random_user_agent, setup_logger

BSB_LOGO = r"""
┳┓┏┓┳┓
┣┫┗┓┣┫
┻┛┗┛┻┛
      """

class AdminFinder:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.parsed = urlparse(self.base_url)
        self.domain = self.parsed.netloc.replace(':', '_')
        self.logger = setup_logger('admin_finder')
        cfg = load_config()
        self.timeout = cfg.get('DEFAULT_TIMEOUT', 10)
        self.thread_count = cfg.get('THREAD_COUNT', 10)
        self.paths = cfg.get('ADMIN_PATH_WORDLIST', [])
        self.headers = {'User-Agent': get_random_user_agent()}
        self.found = queue.Queue()

    def worker(self):
        while True:
            try:
                path = self.queue.get(block=False)
            except queue.Empty:
                return

            full_url = urljoin(self.base_url, path)
            try:
                resp = requests.get(full_url, headers=self.headers, timeout=self.timeout, allow_redirects=False)
                self.logger.info(f"Checked {full_url} -> Status: {resp.status_code}")
                if resp.status_code == 200:
                    self.found.put(full_url)
                    cprint(f"[BSB] Found possible admin page: {full_url}", "red")
                else:
                    self.logger.debug(f"No admin page at {full_url}")
            except Exception as e:
                self.logger.error(f"Error checking {full_url}: {e}")
            finally:
                self.queue.task_done()

    def run(self):
        cprint(BSB_LOGO, "cyan")
        cprint(f"[BSB] Starting multithreaded admin panel scan on: {self.base_url}", "green")

        self.queue = queue.Queue()
        for path in self.paths:
            self.queue.put(path)

        threads = []
        for _ in range(self.thread_count):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)

        self.queue.join()

        if self.found.empty():
            cprint("[BSB] No common admin pages found.", "blue")
            self.logger.info(f"No admin panel found on {self.base_url}")
        else:
            total = self.found.qsize()
            cprint(f"[BSB] Total admin pages found: {total}", "cyan")
            self.logger.warning(f"Total admin pages found: {total}")

def main():
    if len(sys.argv) != 2:
        cprint("Usage: black-a <base_url>", "yellow")
        return
    finder = AdminFinder(sys.argv[1])
    finder.run()
