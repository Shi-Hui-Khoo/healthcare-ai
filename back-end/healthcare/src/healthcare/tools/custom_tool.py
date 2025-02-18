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
        info = json.loads(appointment)
        print("Extracted information - ",info)
        missing_keys = [ x for x in info.keys() if x in self.essential_keys]
        print("Missing information - ",missing_keys)
        # Implementation goes here
        try:
            
            #Update user csv
            user_csv_path = "/Users/ammarsyatbi/repo/healthive-hackathon/healthcare/knowledge/patient.csv"
            user_df = pd.read_csv(user_csv_path)
            patient_id = str(len(user_df)+1)
            
            # columns - patient_id,patient_name,age,email,phone
            user_df.loc[len(user_df)] = [patient_id, info['user_name'], info['age'], "sample@email.com", "012347xxxx"]
            user_df.to_csv(user_csv_path, index=False)

            #Update appt csv
            appt_csv_path = "/Users/ammarsyatbi/repo/healthive-hackathon/healthcare/knowledge/appointment.csv"
            appt_df = pd.read_csv(appt_csv_path)
            dr_df = pd.read_csv("/Users/ammarsyatbi/repo/healthive-hackathon/healthcare/knowledge/doctor.csv")
            doctor_id = dr_df[dr_df.doctor_name.str.strip() == 'Dr. John Smith'].doctor_id.iloc[0]
            doctor_id = str(doctor_id)
            #columns - appointment_id,doctor_id,patient_id,patient_symptom,insurance,date,time
            appt_df.loc[len(appt_df)] = [patient_id, doctor_id, info['symptoms'], info['insurance_name'], info['appt_dat'], info['appt_time']]
            appt_df.to_csv(appt_csv_path, index=False)

            #Update timeslot csv
            timeslot_csv_path = "/Users/ammarsyatbi/repo/healthive-hackathon/healthcare/knowledge/doctor_timeslot.csv"
            timeslot_df = pd.read(timeslot_csv_path)
            # columns - doctor_id,date,time
            # removes available timeslot
            timeslot_df = timeslot_df[~(timeslot_df.doctor_id.astype(str) == doctor_id) & 
                        (timeslot_df.date == info['appt_date']) & 
                        (timeslot_df.time == info['appt_time'])]
            timeslot_df.to_csv(timeslot_csv_path, index=False)

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
