from utils import Statuses,Logg,ProjectUtils
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from routers import users,views
from fastapi.openapi.utils import get_openapi

app=FastAPI()
Logg().logSetup()

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
    
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.middleware("http")
async def log_request(request, call_next):
    response = await call_next(request)
    ProjectUtils.print_log_msg(f'{request.method} {request.url} '+f'Status code: {response.status_code}',logger="SERVER")
    return response

app.include_router(users.router,tags=['users'])
app.include_router(views.router,tags=['views'])


