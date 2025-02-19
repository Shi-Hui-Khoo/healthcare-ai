from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.healthcare.tools.custom_tool import UpdateCSV

from dotenv import load_dotenv, find_dotenv
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

@CrewBase
class AdminCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    csv_updater = UpdateCSV()

    @agent
    def healthcare_admin(self) -> Agent:
        return Agent(config=self.agents_config["healthcare_admin"], 
                     llm=llm, 
                     allow_delegation=False, 
                     max_iter=2, 
                     verbose=True)
    
    @agent
    def appointment_admin(self) -> Agent:
        return Agent(config=self.agents_config["healthcare_admin"], 
                     llm=llm, 
                     allow_delegation=False, 
                     max_iter=2, 
                     verbose=True, 
                     tools=[self.csv_updater])

    @task
    def route_task(self) -> Task:
        return Task(
            config=self.tasks_config["route_task"],
        )

    @task
    def collect_task(self) -> Task:
        return Task(config=self.tasks_config["collect_task"])
    
    @task
    def extract_task(self) -> Task:
        return Task(config=self.tasks_config["extract_task"])
    
    @task
    def update_task(self) -> Task:
        return Task(config=self.tasks_config["update_task"])
    
    @task
    def summarize_task(self) -> Task:
        return Task(config=self.tasks_config["summarize_task"])

    @crew
    def crew(self, mode='route') -> Crew:
        """Creates the Healthhive crew"""
        if mode == 'route':
            return Crew(
                agents=[self.healthcare_admin()],
                tasks=[self.route_task()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == 'collect':
            return Crew(
                agents=[self.healthcare_admin()],
                tasks=[self.collect_task()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == 'update':
            return Crew(
                agents=[self.appointment_admin(), self.healthcare_admin()],
                tasks=[self.extract_task(), self.update_task(), self.summarize_task()],
                process=Process.sequential,
                verbose=True,
            )