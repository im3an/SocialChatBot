import random
import os
from dotenv import load_dotenv

class ProxyManager:
    def __init__(self, proxy_list=None):
        load_dotenv()
        # Load proxies from .env or use provided list
        proxies_env = os.getenv('INSTAGRAM_PROXIES')
        if proxy_list:
            self.proxies = proxy_list
        elif proxies_env:
            self.proxies = [p.strip() for p in proxies_env.split(',') if p.strip()]
        else:
            self.proxies = []
        self.index = 0

    def get_random_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def get_next_proxy(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.index]
        self.index = (self.index + 1) % len(self.proxies)
        return proxy

    def add_proxy(self, proxy):
        if proxy not in self.proxies:
            self.proxies.append(proxy)

    def remove_proxy(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy) 