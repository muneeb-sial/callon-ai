from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

fastapi_instance = FastAPI()

fastapi_instance.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
