import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx

load_dotenv()
KEY = os.environ["KEY"]

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def proxy(url: str, key: str):
    if key != KEY:
        return "Access denied"

    async with httpx.AsyncClient() as client:
        return (await client.get(url)).text


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8000))
