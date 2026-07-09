import json
import os
import time
from config import DATA_FOLDER

CACHE_FILE = os.path.join(DATA_FOLDER, "notification_cache.json")


def _load_cache():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def _save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f)


def can_send(symbol, cooldown):
    cache = _load_cache()

    now = time.time()

    if symbol not in cache:
        cache[symbol] = now
        _save_cache(cache)
        return True

    if now - cache[symbol] >= cooldown:
        cache[symbol] = now
        _save_cache(cache)
        return True

    return False
