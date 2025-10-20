from fastapi import FastAPI
from api.routers import file_router
import os

app = FastAPI(title="Tampered Document AI Detector")

app.include_router(file_router.router)

@app.get("/")
def root():
    return {
        "message": "Hello World!",
        "cwd": os.getcwd()
    }
