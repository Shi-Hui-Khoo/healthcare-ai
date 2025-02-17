from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from .base import router, openapi_update

import logging

logging.basicConfig(level=logging.INFO)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/openapi.json")
async def openapi():
    return get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)

@app.get("/docs")
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

app.add_api_route("/openapi", endpoint=openapi_update)
app.include_router(router)