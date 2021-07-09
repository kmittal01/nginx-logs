import uvicorn
from column.app.v1.auth.routes import auth_router
from column.app.v1.core import config
from column.app.v1.core.auth import get_current_active_user
from column.app.v1.core.config import API_PREFIX
from column.app.v1.nginx_logs.routes import nginx_logs_router
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


connect('column', host='mongo', port=27017, username="column", password="password", authentication_source='admin')

app.include_router(auth_router, prefix=API_PREFIX, tags=["auth"])


app.include_router(
    nginx_logs_router,
    prefix=API_PREFIX,
    tags=["Nginx Logs"],
    dependencies=[Depends(get_current_active_user)],
)

if __name__ == "__main__":
    uvicorn.run("manage:app", host="0.0.0.0", reload=True, port=8888)
