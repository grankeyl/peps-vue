from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiocache import SimpleMemoryCache
from fastapi.staticfiles import StaticFiles

import asyncio
import uvicorn

''' FastAPI APP '''
app = FastAPI()
port = 5300
cache = SimpleMemoryCache()

app.mount("/static", StaticFiles(directory="./static"), name="static")

from routes.routes import home_panel

app.include_router(home_panel)

origins = [
    f"http://localhost",
    f"http://localhost:{port}",
    f"http://127.0.0.1:{port}",
    f"http://192.168.0.123:{port}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=port, loop="uvloop")