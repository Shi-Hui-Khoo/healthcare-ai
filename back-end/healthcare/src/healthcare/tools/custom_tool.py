from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List
import json
import pandas as pd

class Appointment(BaseModel):
    """Input schema for MyCustomTool."""

    appointment: str = Field(..., description="JSON string of appointment information.")


class UpdateCSV(BaseTool):
    name: str = "csv_update"
    essential_keys: List[str] = ['user_name', 'age','gender', 'insurance_name', 'symptoms', 'dr_name', 'appt_date','appt_time']
    description: str = (
        "This is used to update csv using pandas based on provided dictionary. The keys in the dictionary will be determine to which columns or csv updated."
    )
    args_schema: Type[BaseModel] = Appointment

    def _run(self, appointment: str) -> str:
        print("Updating CSV")
        info = json.loads(appointment)
        print("Extracted information - ",info)
        missing_keys = [ x for x in info.keys() if x not in self.essential_keys]
        print("Missing information - ",missing_keys)
        # Implementation goes here
        try:
            
            #Update user csv
            user_csv_path = "knowledge/patient.csv"
            user_df = pd.read_csv(user_csv_path)
            print(f"Updating patient, patient row - {user_df.shape[0]}")
            patient_id = str(len(user_df)+1)
            
            # columns - patient_id,patient_name,age,email,phone
            user_df.loc[len(user_df)] = [patient_id, info['user_name'], info['age'], "sample@email.com", "012347xxxx"]
            user_df.to_csv(user_csv_path, index=False)
            print(f"Patient's updated, patient row - {user_df.shape[0]}")

            #Update appt csv
            appt_csv_path = "knowledge/appointments.csv"
            appt_df = pd.read_csv(appt_csv_path)
            print(f"Updating appointment, appt row - {appt_df.shape[0]}")

            dr_df = pd.read_csv("knowledge/doctor.csv")
            doctor_id = dr_df[dr_df.doctor_name.str.strip() == info['dr_name'] ].doctor_id.iloc[0]
            doctor_id = str(doctor_id)
            appt_id = str(len(appt_df)+1)
            #columns - appointment_id,doctor_id,patient_id,patient_symptom,insurance,date,time
            appt_df.loc[len(appt_df)] = [appt_id, patient_id, doctor_id, info['symptoms'], info['insurance_name'], "12/02/2025", info['appt_time']]
            appt_df.to_csv(appt_csv_path, index=False)
            
            print(f"Appointment's updated. Appt row - {appt_df.shape[0]}.")
            print(f"Doctor id - {doctor_id}, Appt id - {appt_id}, Patient id - {patient_id}")

            #Update timeslot csv
            timeslot_csv_path = "knowledge/doctor_timeslot.csv"
            timeslot_df = pd.read_csv(timeslot_csv_path)
            print(f"Updating timeslot, timeslot row - {timeslot_df.shape[0]}")

            # columns - doctor_id,date,time
            # removes available timeslot
            timeslot_df = timeslot_df[~((timeslot_df.doctor_id.astype(str) == doctor_id) & 
                        (timeslot_df.date == "12/02/2025") & 
                        (timeslot_df.time == info['appt_time']))]
            timeslot_df.to_csv(timeslot_csv_path, index=False)
            print(f"Timeslot's updated, timeslot row - {timeslot_df.shape[0]}")

            return "All csv has been updated."
        except Exception as e:
            return e
        


# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""

#     argument: str = Field(..., description="Description of the argument.")


# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, your agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."
