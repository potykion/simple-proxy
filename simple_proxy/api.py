import re
from dataclasses import dataclass, asdict
from typing import Any
from urllib.parse import urlparse, urljoin, urlencode


@dataclass
class ProxyUrl:
    """
    >>> ProxyUrl("http://localhost:8000/", "1488", "https://google.com").url
    'http://localhost:8000/proxy?key=1488&url=https%3A%2F%2Fgoogle.com'
    """
    base_url: str
    key: str
    url_to_proxy: str
    path: str = "/proxy"

    @property
    def url(self) -> str:
        return f"{urljoin(self.base_url, self.path)}?{urlencode({'key': self.key, 'url': self.url_to_proxy})}"

    def copy_with(self, **kwargs: Any) -> 'ProxyUrl':
        return ProxyUrl(**{**asdict(self), **kwargs})

    def set_path(self, path: str) -> 'ProxyUrl':
        """
        >>> ProxyUrl("http://localhost:8000/", "1488", "https://google.com").set_path("/search").url
        'http://localhost:8000/proxy?key=1488&url=https%3A%2F%2Fgoogle.com%2Fsearch'
        >>> ProxyUrl("http://localhost:8000/", "1488", "https://google.com/search/howsearchworks/?fg=1").set_path("/search").url
        'http://localhost:8000/proxy?key=1488&url=https%3A%2F%2Fgoogle.com%2Fsearch'
        >>> ProxyUrl("http://localhost:8000/", "1488", "https://google.com").set_path("search").url
        'http://localhost:8000/proxy?key=1488&url=https%3A%2F%2Fgoogle.com%2Fsearch'
        """
        return self.copy_with(url_to_proxy=urljoin(extract_base_url(self.url_to_proxy), path))


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

    >>> replace_relative_urls('href="/logo.png"', ProxyUrl("http://localhost:8000", "1", "https://google.com"))
    'href="http://localhost:8000/proxy?key=1&url=https%3A%2F%2Fgoogle.com%2Flogo.png"'
    >>> replace_relative_urls('src="/logo.png"', ProxyUrl("http://localhost:8000", "1", "https://google.com"))
    'src="http://localhost:8000/proxy?key=1&url=https%3A%2F%2Fgoogle.com%2Flogo.png"'
    """
    replaced_html = re.sub(r'src="/(.*?)"', lambda m: f'src="{proxy_url.set_path(m.group(1)).url}"', html)
    replaced_html = re.sub(r'href="/(.*?)"', lambda m: f'href="{proxy_url.set_path(m.group(1)).url}"', replaced_html)
    return replaced_html
