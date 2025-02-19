from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool

from dotenv import load_dotenv, find_dotenv

import pandas as pd
import os

load_dotenv(find_dotenv())

# Parameters
parameters = {"decoding_method": "greedy", "max_new_tokens": 500}
llm = LLM(
    model="watsonx/meta-llama/llama-3-3-70b-instruct",
    base_url="https://us-south.ml.cloud.ibm.com",
    params=parameters,
    project_id=os.getenv("WATSONX_PROJECT_ID", None),
    apikey=os.getenv("WATSONX_API_KEY", None),
)
function_calling_llm = LLM(
    model="watsonx/ibm-mistralai/merlinite-7b",
    base_url="https://us-south.ml.cloud.ibm.com",
    params=parameters,
    project_id=os.getenv("WATSONX_PROJECT_ID", None),
    apikey=os.getenv("WATSONX_API_KEY", None),
)

@CrewBase
class MedicalCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # tools
    # Using ollama atm since watson has an unresolved issue -https://github.com/crewAIInc/crewAI/issues/1770
    medical_condition_reference = CSVSearchTool(
        csv="knowledge/medical_condition.csv",
        description="Use this tool to extract medical condition from CSV",
        config=dict(
            llm=dict(
                provider="ollama",  # or google, openai, anthropic, llama2, ...
                config=dict(
                    model="llama3",
                    base_url="http://0.0.0.0:11434",
                    # temperature=0.5,
                    # top_p=1,
                    # stream=true,
                ),
            ),
            embedder=dict(
                provider="ollama",  # or openai, ollama, ...
                config=dict(
                    model="mxbai-embed-large",
                    # task_type="retrieval_document",
                    # title="Embeddings",
                ),
            ),
        ),
    )
    suggested_doctor = CSVSearchTool(
        csv="knowledge/doctor.csv",
        description="Use this tool to find relevant doctors from provided symptoms or illness",
        config=dict(
            llm=dict(
                provider="ollama",  # or google, openai, anthropic, llama2, ...
                config=dict(
                    model="llama3",
                    base_url="http://0.0.0.0:11434",
                    # temperature=0.5,
                    # top_p=1,
                    # stream=true,
                ),
            ),
            embedder=dict(
                provider="ollama",  # or openai, ollama, ...
                config=dict(
                    model="mxbai-embed-large",
                    # task_type="retrieval_document",
                    # title="Embeddings",
                ),
            ),
        ),
    )

    timeslot = CSVSearchTool(
        csv="knowledge/doctor_timeslot.csv",
        description="Use this tool to extract doctor's available timeslot from doctor's id.",
        config=dict(
            llm=dict(
                provider="ollama",  # or google, openai, anthropic, llama2, ...
                config=dict(
                    model="llama3",
                    base_url="http://0.0.0.0:11434",
                    # temperature=0.5,
                    # top_p=1,
                    # stream=true,
                ),
            ),
            embedder=dict(
                provider="ollama",  # or openai, ollama, ...
                config=dict(
                    model="mxbai-embed-large",
                    # task_type="retrieval_document",
                    # title="Embeddings",
                ),
            ),
        ),
    )

    @agent
    def medical_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["medical_assistant"],
            max_iter=1,
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def csv_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["csv_agent"],
            tools=[
                self.suggested_doctor,
                self.timeslot,
            ],
            verbose=True,
            allow_delegation=False,
            max_iter=2,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def get_medical_reference_task(self) -> Task:
        # TODO: get illness descripton tools
        return Task(config=self.tasks_config["get_medical_reference"])

    @task
    def classify_illness_task(self) -> Task:
        # TODO: get illness descripton tools
        return Task(config=self.tasks_config["classify_illness_task"])

    @task
    def get_suggested_doctor(self) -> Task:
        # TODO: get doctor's specialization
        return Task(config=self.tasks_config["get_suggested_doctor"])

    @task
    def get_doctor_timeslot_task(self) -> Task:
        return Task(config=self.tasks_config["get_doctor_timeslot_task"])

    @task
    def suggest_timeslot(self) -> Task:
        return Task(config=self.tasks_config["suggest_timeslot"])

    # @tool
    # def get_doctor_timeslot_tool(doctors: list) -> str:
    #     """Match available doctors from CSV and return the free time"""
    #     df = pd.read_csv("csv_location")
    #     available_drs = df[df.doctors.isin(doctors)]['doctor_name','slot']

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.medical_assistant(), self.csv_agent()],
            tasks=[
                self.classify_illness_task(),
                self.get_suggested_doctor(),
                self.get_doctor_timeslot_task(),
                self.suggest_timeslot(),
            ],
            process=Process.sequential,
            verbose=1,
        )
