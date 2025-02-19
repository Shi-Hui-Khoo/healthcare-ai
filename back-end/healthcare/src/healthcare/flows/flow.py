from pydantic import BaseModel
from typing import Any, Mapping, List
from crewai.flow import Flow, listen, start


from src.healthcare.crews.admin_crew.admin_crew import AdminCrew
from src.healthcare.crews.medical_crew.medical_crew import MedicalCrew

class CollectState(BaseModel):
    route: str | None = None
    context: str | None = ""
    query: str | None = None
    inputs: List[Mapping[str, Any]] | None = None
    # inputs: str | None= ""


class RouterFlow(Flow[CollectState]):
    @start("start")
    def converse(self):
        print("Starting the collector flow")
        self.state.route = "start"
        self.state.inputs = "\n".join(
            [
                f"user: {c['u']}" if 'u' in c else f"assistant: {c['a']}" for c in self.state.inputs
            ]
        )
        print(self.state.inputs)

    # router still broken atm
    @listen(converse)
    def route_task(self):
        #Routing aka planning task.
        result = (
            AdminCrew().crew(mode='route').kickoff(inputs={"conversation": self.state.inputs})
        )
        result = str(result).strip()
        self.state.route = result
        print(f"route task - '{self.state.route}'")

    @listen(route_task)
    def run_task(self):
        print("run task")
        if self.state.route in ["background", "symptoms", "clarify"]:
            # Information collection task
            result = (
                AdminCrew()
                .crew(mode='collect')
                .kickoff(
                    inputs={
                        "task": self.state.route,
                        "context": self.state.context,
                        "conversation": self.state.inputs,
                    }
                )
            )
        elif self.state.route == 'schedule':
            # Timeslot suggestion task
            result = (
            MedicalCrew()
            .crew()
            .kickoff(inputs={"conversation": self.state.inputs})
        )
        elif self.state.route == 'complete':
            print("conversation completed.")
            # Extract, update and summarize task
            result = (
                AdminCrew()
                .crew(mode='update')
                .kickoff(
                    inputs={
                        "task": self.state.route,
                        "context": self.state.context,
                        "conversation": self.state.inputs,
                    }
                )
            )

        self.state.query = str(result)

    @listen(run_task)
    def complete_task(self):
        print("complete conversation")
        if self.state.query:
            return self.state.query
        return """Sorry. We could not understand your query. Could please rephrase your question?"""