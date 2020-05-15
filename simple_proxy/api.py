import re
from dataclasses import dataclass, asdict
from typing import List, Dict
from urllib.parse import urlparse, urljoin


@dataclass
class ProxyUrl:
    """
    >>> ProxyUrl("http://localhost:8000/", "1488", "https://google.com").url
    'http://localhost:8000/1488/proxy/https://google.com'
    >>> ProxyUrl("http://localhost:8000/", "1488", "https://google.com/search").url_with_base_url
    'http://localhost:8000/1488/proxy/https://google.com'
    """
    base_url: str
    key: str
    url_to_proxy: str

    @property
    def url(self) -> str:
        return f"{urljoin(self.base_url, self.key)}/proxy/{self.url_to_proxy}"

    @property
    def url_with_base_url(self) -> str:
        return ProxyUrl(**{**asdict(self), "url_to_proxy": extract_base_url(self.url_to_proxy)}).url


def extract_base_url(url: str) -> str:
    """
    >>> extract_base_url("https://fastapi.tiangolo.com/advanced/using-request-directly/#use-the-request-object-directly")
    'https://fastapi.tiangolo.com'
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.hostname}"


def replace_relative_urls(html: str, proxy_url: ProxyUrl) -> str:
    """
    Replace relative urls from src and href with absolute proxy urls
    (/logo.png > http://localhost:8000?key={key}&url={base_url}/logo.png)
    """
    url = proxy_url.url_with_base_url
    replaced_html = re.sub(r'src="/(.*?)"', fr'src="{url}/\1"', html)
    replaced_html = re.sub(r'href="/(.*?)"', fr'href="{url}/\1"', replaced_html)
    return replaced_html
