import json
import os
import random
import logging
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

# ১) লোড কনফিগারেশন
def load_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load config.json: {e}")
        return {}

# ২) র্যান্ডম ইউজার-এজেন্ট
def get_random_user_agent():
    config = load_config()
    agents = config.get('USER_AGENT_LIST', [])
    return random.choice(agents) if agents else 'python-requests/2.x'

# ৩) লগ ব্যবস্থা (সব মডিউলেও ব্যবহারযোগ্য)
def setup_logger(module_name):
    logs_dir = os.path.join(BASE_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, f"{module_name}_{datetime.now():%Y%m%d_%H%M%S}.log")

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
