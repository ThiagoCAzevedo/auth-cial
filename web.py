from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from modules.create.api.routes import router as register_router
from modules.read.api.routes import router as list_router
from modules.update.api.routes import router as login_router
from modules.delete.api.routes import router as delete_router


app = FastAPI(
    title="Auth Auto Line Feeding", 
    docs_url="/auth-doc",
    description="Auth microservice for Auto Line Feeding System"
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


# -- REGISTER ROUTES --
app.include_router(register_router, prefix="/user/register", tags=["register"])


# -- LIST ROUTES --
app.include_router(list_router, prefix="/admin", tags=["list"])


# -- LOGIN ROUTES --
app.include_router(login_router, prefix="/user/login", tags=["login"])


# -- DELETE ROUTES --
app.include_router(delete_router, prefix="/admin/delete", tags=["delete"])
