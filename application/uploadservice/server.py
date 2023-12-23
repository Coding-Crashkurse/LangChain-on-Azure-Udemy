import logging
import os

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

# Logger configuration
logger = logging.getLogger("proxy_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProxyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define a list of endpoints that need to be proxied
        proxied_endpoints = [
            "/conversation",
            "/deletefile",
            "/listfiles",
            "/uploadfiles",
        ]

        if any(request.url.path.startswith(endpoint) for endpoint in proxied_endpoints):
            proxy_target = os.getenv("TARGET", "http://backend:5000")

            path = str(request.url).replace(str(request.base_url), "")
            proxy_url = f"{proxy_target.rstrip('/')}/{path.lstrip('/')}"

            print("PROXY_TARGET: ", proxy_url)

            logger.info(f"Proxying to {proxy_url}")

            headers = {
                key: value for key, value in request.headers.items() if key != "host"
            }

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


# Add the modified middleware
app.add_middleware(ProxyMiddleware)

# Serve static files
app.mount("", StaticFiles(directory="dist/uploadservice", html=True), name="static")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
