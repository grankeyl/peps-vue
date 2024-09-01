from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiocache import SimpleMemoryCache
from fastapi.responses import JSONResponse
import uvicorn
from config import CreateConfig

app = FastAPI()
cache = SimpleMemoryCache()
config = CreateConfig()


from routes.user import router_user
from routes.shop import shop as router_shop

app.include_router(router_user)
app.include_router(router_shop)

origins = [
    "http://localhost",
    "http://localhost:7000",
    "http://localhost:8080",
    "http://127.0.0.1:7000",
    "http://127.0.0.1:8080",
    "http://192.168.0.123:7000",
    "http://192.168.0.123:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)