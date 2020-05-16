import os

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from simple_proxy.api import replace_relative_urls, ProxyUrl

load_dotenv()
KEY = os.environ["KEY"]

app = FastAPI()


@app.get(ProxyUrl.path)
async def proxy(key: str, url: str):
    """Get content of given {url}"""
    if key != KEY:
        return "Access denied"

    async with httpx.AsyncClient() as client:
        return Response((await client.get(url)).read())


@app.get("/html", response_class=HTMLResponse)
async def html_proxy(key: str, url: str, request: Request):
    """Get content of given html {url} with relative urls replace"""
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
