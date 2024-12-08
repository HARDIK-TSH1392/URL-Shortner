import hashlib
import time
from urllib.parse import urlparse
from threading import Lock
import requests


class URLShortener:
    def __init__(self, base_url="http://localhost:5001/"):
        if not self._is_valid_base_url(base_url):
            raise ValueError("Invalid base URL provided")
        self.base_url = base_url
        self.url_map = {}
        self.stats = {}
        self.ttl_map = {}
        self.lock = Lock()

    def _generate_short_url(self, long_url):
        if not long_url:
            raise ValueError("Long URL cannot be empty")
        return hashlib.md5(long_url.encode()).hexdigest()[:8]

    def shorten_url(self, long_url, ttl=None):
        if not self._is_valid_url(long_url):
            raise ValueError("Invalid or unreachable URL")

        short_url_key = self._generate_short_url(long_url)

        with self.lock:
            if short_url_key not in self.url_map:
                self.url_map[short_url_key] = long_url
                self.stats[short_url_key] = 0
                if ttl:
                    if not isinstance(ttl, (int, float)) or ttl <= 0:
                        raise ValueError("TTL must be a positive number")
                    self.ttl_map[short_url_key] = time.time() + ttl

        return self.base_url + short_url_key

    def redirect(self, short_url_key):
        with self.lock:
            if short_url_key in self.ttl_map and time.time() > self.ttl_map[short_url_key]:
                self._cleanup(short_url_key)
                return None

            if short_url_key in self.url_map:
                self.stats[short_url_key] += 1
                return self.url_map[short_url_key]

        return None

    def get_stats(self, short_url_key):
        with self.lock:
            if short_url_key in self.stats:
                return {"access_count": self.stats[short_url_key]}

        return None

    def _is_valid_url(self, url):
        try:
            parsed = urlparse(url)
            if not (parsed.netloc and parsed.scheme):
                return False
            response = requests.head(url, timeout=5)
            return response.status_code < 400
        except Exception:
            return False

    def _is_valid_base_url(self, base_url):
        try:
            parsed = urlparse(base_url)
            return bool(parsed.netloc) and bool(parsed.scheme) and base_url.endswith("/")
        except Exception:
            return False

    def _cleanup(self, short_url_key):
        if short_url_key in self.url_map:
            del self.url_map[short_url_key]
        if short_url_key in self.stats:
            del self.stats[short_url_key]
        if short_url_key in self.ttl_map:
            del self.ttl_map[short_url_key]
