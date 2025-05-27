import requests
import threading
import time

PROXY_SOURCES = [
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://www.proxy-list.download/api/v1/get?type=http',
    'https://www.proxyscan.io/download?type=http',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
]

PROXY_FILE = 'working_proxies.txt'

class ProxyScraper:
    def __init__(self, test_url='https://httpbin.org/ip', timeout=5):
        self.test_url = test_url
        self.timeout = timeout
        self.working_proxies = set()

    def fetch_proxies(self):
        proxies = set()
        for url in PROXY_SOURCES:
            try:
                print(f"[ProxyScraper] Fetching proxies from {url}")
                resp = requests.get(url, timeout=10)
                for line in resp.text.splitlines():
                    proxy = line.strip()
                    if proxy:
                        proxies.add(proxy)
            except Exception as e:
                print(f"[ProxyScraper] Failed to fetch from {url}: {e}")
        print(f"[ProxyScraper] Fetched {len(proxies)} proxies from all sources.")
        return proxies

    def verify_proxy(self, proxy):
        try:
            resp = requests.get(self.test_url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=self.timeout)
            if resp.status_code == 200:
                print(f"[ProxyScraper] Working proxy: {proxy}")
                return True
        except Exception:
            pass
        return False

    def update_working_proxies(self):
        proxies = self.fetch_proxies()
        self.working_proxies = set()
        for proxy in proxies:
            if self.verify_proxy(proxy):
                self.working_proxies.add(proxy)
        with open(PROXY_FILE, 'w') as f:
            for proxy in self.working_proxies:
                f.write(proxy + '\n')
        print(f"[ProxyScraper] Saved {len(self.working_proxies)} working proxies to {PROXY_FILE}")

    def start_periodic_update(self, interval=1800):
        def run():
            while True:
                print("[ProxyScraper] Starting proxy update...")
                self.update_working_proxies()
                print("[ProxyScraper] Proxy update complete. Sleeping...")
                time.sleep(interval)
        thread = threading.Thread(target=run, daemon=True)
        thread.start() 