import os

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from simple_proxy.api import replace_relative_urls, ProxyUrl

load_dotenv()
KEY = os.environ["KEY"]

app = FastAPI()


@app.get("/{key}/proxy/{url:path}", response_class=HTMLResponse)
async def proxy(key: str, url: str):
    """Read and display content of given {url}, replace relative links if {replace_relative}"""
    if key != KEY:
        return "Access denied"

    async with httpx.AsyncClient() as client:
        text = (await client.get(url)).text

    return text


@app.get("/{key}/proxy-full/{url:path}", response_class=HTMLResponse)
async def proxy_full(key: str, url: str, request: Request):
    if key != KEY:
        return "Access denied"

    async with httpx.AsyncClient() as client:
        text = (await client.get(url)).text

    text = replace_relative_urls(
        text,
        ProxyUrl(str(request.base_url), key=key, url_to_proxy=url),
    )
    return text


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8000))
