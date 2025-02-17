from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
import requests
from .utils import Request, Response
from src.healthcare.flows.flow import RouterFlow
import os 

router = APIRouter()
flow = RouterFlow()

LIMIT_WINDOW = 15 

# Seperately run as frontend
# @router.get("/")
# async def page_home():
#     return FileResponse('static/home.html')

# @router.get("/main")
# async def page_main():
#     return FileResponse('static/main.html')

@router.post("/api/agent_flow")
def flow(request: Request) -> Response:
    history = request.history[:LIMIT_WINDOW]

    result = flow.kickoff(inputs={"inputs": history})
    
    return result

def openapi_update(request: Request):
    url = request.base_url._url[:-1]
    openapi = requests.get(f"{url}/openapi.json").json()
    openapi["openapi"] = "3.0.3"
    openapi["info"] = {
        "title": "watsonx.ai generation API endpoint",
        "version": "0.1.0",
    }
    openapi["servers"] = [{"url": url, "description": "watsonx.ai endpoint"}]
    # if "paths" in openapi:
    #     del openapi["paths"]["/"]
    if "/openapi" in openapi["paths"]:
        del openapi["paths"]["/openapi"]
    for x in [x for x in openapi["paths"] if not x.startswith("/api")]:
        del openapi["paths"][x]
    if "components" in openapi:
        del openapi["components"]["schemas"]["HTTPValidationError"]
        del openapi["components"]["schemas"]["ValidationError"]
        openapi["components"]["securitySchemes"] = {"basicAuth": {"type": "http", "scheme": "basic"}}
    for k in openapi["paths"].keys():
        if "post" in openapi["paths"][k]:
            del openapi["paths"][k]["post"]["responses"]["422"]
    return openapi