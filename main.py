import uvicorn
from fastapi import FastAPI

from src.config.settings import DEBUG
from src.routers.base_router import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=DEBUG)
