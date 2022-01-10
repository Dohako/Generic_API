from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.data_handler import handle_data

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:8080",
    "localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to todo generic API"}

@app.post("/get_info", tags=["get_info"])
async def get_info(base_request:dict) -> dict:
    result = handle_data(base_request)
    return {"data" : result}
