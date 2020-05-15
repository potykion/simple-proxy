import os

from simple_proxy.api import replace_relative_urls, ProxyUrl


def test_replace_urls(test_data_dir: str) -> None:
    with open(os.path.join(test_data_dir, "google.html"), encoding="utf-8") as f:
        html = f.read()

    html_with_replaced_urls = replace_relative_urls(
        html,
        ProxyUrl("http://localhost:8000/", "1488", "https://google.com/"),
    )

    # with open(os.path.join(test_data_dir, "google_with_replaced_url.html"), "w") as f:
    #     f.write(html_with_replaced_urls)

    with open(os.path.join(test_data_dir, "google_with_replaced_url.html"), encoding="utf-8") as f:
        expected = f.read()

    assert html_with_replaced_urls == expected
