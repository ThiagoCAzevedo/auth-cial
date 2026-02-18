from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from .routes import *


app = FastAPI(
    title="Auth Auto Line Feeding", 
    docs_url="/auth-doc",
    description="Auth microservice for Auto Line Feeding System"
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


app.include_router(users_router, prefix="/users", tags=["users"])
