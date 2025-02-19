from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import requests
from .utils import AgentRequest, AgentResponse
from src.healthcare.flows.flow import RouterFlow
import os 
import pandas as pd

router = APIRouter()


LIMIT_WINDOW = 15 

# Seperately run as frontend
# @router.get("/")
# async def page_home():
#     return FileResponse('static/home.html')

# @router.get("/main")
# async def page_main():
#     return FileResponse('static/main.html')

@router.get("/csv/patient", response_class=HTMLResponse)
async def read_patient():
    df = pd.read_csv("knowledge/patient.csv")
    return df.to_html()

@router.get("/csv/doctor", response_class=HTMLResponse)
async def read_patient():
    df = pd.read_csv("knowledge/doctor.csv")
    return df.to_html()

@router.get("/csv/timeslot", response_class=HTMLResponse)
async def read_patient():
    df = pd.read_csv("knowledge/doctor_timeslot.csv")
    return df.to_html()

@router.get("/csv/appointment", response_class=HTMLResponse)
async def read_patient():
    df = pd.read_csv("knowledge/appointments.csv")
    return df.to_html()

@router.post("/api/agent_flow")
def flow(request: AgentRequest) -> AgentResponse:
    history = request.history[:LIMIT_WINDOW]

    flow = RouterFlow()
    result = flow.kickoff(inputs={"inputs": history})
    
    return {"response":result}

# def openapi_update(request: Request):
#     url = request.base_url._url[:-1]
#     openapi = requests.get(f"{url}/openapi.json").json()
#     openapi["openapi"] = "3.0.3"
#     openapi["info"] = {
#         "title": "watsonx.ai generation API endpoint",
#         "version": "0.1.0",
#     }
#     openapi["servers"] = [{"url": url, "description": "watsonx.ai endpoint"}]
#     # if "paths" in openapi:
#     #     del openapi["paths"]["/"]
#     if "/openapi" in openapi["paths"]:
#         del openapi["paths"]["/openapi"]
#     for x in [x for x in openapi["paths"] if not x.startswith("/api")]:
#         del openapi["paths"][x]
#     if "components" in openapi:
#         del openapi["components"]["schemas"]["HTTPValidationError"]
#         del openapi["components"]["schemas"]["ValidationError"]
#         openapi["components"]["securitySchemes"] = {"basicAuth": {"type": "http", "scheme": "basic"}}
#     for k in openapi["paths"].keys():
#         if "post" in openapi["paths"][k]:
#             del openapi["paths"][k]["post"]["responses"]["422"]
#     return openapi