import logging
import os

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("proxy_logger")
logger.setLevel(logging.INFO)  # Set to logging.DEBUG for more verbose output

handler = logging.StreamHandler()  # Writes to stderr
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


app = FastAPI()

# CORS-Middleware-Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProxyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/conversation"):
            proxy_target = os.getenv("TARGET", "http://backend:5000")
            path = str(request.url).replace(str(request.base_url), "")
            proxy_url = f"{proxy_target.rstrip('/')}/{path.lstrip('/')}"

            print(f"Proxying to {proxy_url}")  # Log the target proxy URL

            headers = {
                key: value for key, value in request.headers.items() if key != "host"
            }
            print(f"Request headers: {headers}")  # Log the headers being forwarded

            try:
                async with httpx.AsyncClient(timeout=20) as client:
                    response = await client.request(
                        method=request.method,
                        url=proxy_url,
                        headers=headers,
                        data=await request.body(),
                        follow_redirects=False,
                    )
                    return HTMLResponse(
                        content=response.content,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                    )
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=500, detail="Backend Communication Failed"
                )
        else:
            return await call_next(request)


app.add_middleware(ProxyMiddleware)

app.mount("", StaticFiles(directory="dist/frontend", html=True), name="static")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
