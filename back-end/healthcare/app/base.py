from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .utils import AgentRequest, AgentResponse
from src.healthcare.flows.flow import RouterFlow
import pandas as pd

router = APIRouter()


LIMIT_WINDOW = 15 

# Front end hosted seperately as nodejs + vue
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

@router.get("/csv/refresh")
async def read_patient():
    try:
        appt = pd.read_csv("knowledge/archive/appointments.csv")
        appt.to_csv("knowledge/appointments.csv", index=False)

        dr = pd.read_csv("knowledge/archive/doctor_timeslot.csv")
        dr.to_csv("knowledge/doctor_timeslot.csv", index=False)
        
        patient = pd.read_csv("knowledge/archive/patient.csv")
        patient.to_csv("knowledge/patient.csv", index=False)
        return "CSV refreshed succcessfully"
    except Exception as e:
        return f"Refresh failed {e}"

@router.post("/api/agent_flow")
def flow(request: AgentRequest) -> AgentResponse:
    history = request.history[:LIMIT_WINDOW]

    flow = RouterFlow()
    result = flow.kickoff(inputs={"inputs": history})
    
    return {"response":result}