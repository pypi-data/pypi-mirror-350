import os
import sys
import threading
import queue
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from termcolor import cprint
from tqdm import tqdm
from .utils import load_config, get_random_user_agent, setup_logger

BSB_LOGO = r"""
┳┓┏┓┳┓
┣┫┗┓┣┫
┻┛┗┛┻┛
      """

# ১) থ্রেড সেফ সেস্ট্রাকচার
class LinkExtractor:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.parsed_base = urlparse(self.base_url)
        self.domain = self.parsed_base.netloc.replace(':', '_')
        self.visited = set()
        self.lock = threading.Lock()
        self.q = queue.Queue()
        self.q.put(self.base_url)
        self.all_links = set()
        self.logger = setup_logger('link_extractor')
        cfg = load_config()
        self.timeout = cfg.get('DEFAULT_TIMEOUT', 10)
        self.thread_count = cfg.get('THREAD_COUNT', 10)

    def fetch_links(self):
        while True:
            try:
                url = self.q.get(block=False)
            except queue.Empty:
                return

            headers = {'User-Agent': get_random_user_agent()}
            try:
                resp = requests.get(url, headers=headers, timeout=self.timeout)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'lxml')
                self.logger.info(f"Fetched: {url} (Status: {resp.status_code})")
                for tag in soup.find_all(['a', 'link', 'script', 'img'], href=True):
                    link = tag.get('href')
                    full_url = urljoin(url, link)
                    parsed = urlparse(full_url)
                    if parsed.scheme in ['http', 'https'] and parsed.netloc == self.parsed_base.netloc:
                        with self.lock:
                            if full_url not in self.visited:
                                self.visited.add(full_url)
                                self.all_links.add(full_url)
                                self.q.put(full_url)
                self.logger.debug(f"Links found on {url}: {len(soup.find_all('a', href=True))}")
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {e}")
            finally:
                self.q.task_done()

    def run(self):
        cprint(BSB_LOGO, "cyan")
        cprint(f"[BSB] Starting multithreaded crawl on: {self.base_url}", "green")
        threads = []
        for _ in range(self.thread_count):
            t = threading.Thread(target=self.fetch_links)
            t.daemon = True
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.save_results()

    def save_results(self):
        folder_name = self.domain
        os.makedirs(folder_name, exist_ok=True)
        file_path = os.path.join(folder_name, "extracted_links.txt")
        with open(file_path, "w") as f:
            for link in sorted(self.all_links):
                f.write(link + "\n")
        cprint(f"[BSB] Links saved in folder: {folder_name}", "cyan")
        self.logger.info(f"[BSB] Total unique links extracted: {len(self.all_links)}")

def main():
    if len(sys.argv) != 2:
        cprint("Usage: black-e <url>", "yellow")
        return
    extractor = LinkExtractor(sys.argv[1])
    extractor.run()
