from datetime import datetime, timedelta
import logging
import os
import json
from crewai import Agent, Task, Crew
from langchain.tools import Tool
from dotenv import load_dotenv

from util.FileUtil import FileUtil

### Static methods
class AgentSummary :

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    # def generate_summary(self, weather_condition_json, suggested_suppliers_json):
    #     weather_condition = json.dumps(weather_condition_json)
    #     suggested_suppliers = json.dumps(suggested_suppliers_json)
        
    #     result = {
    #         "summary": {
    #             "weather_condition": weather_condition,
    #             "suggested_suppliers": suggested_suppliers["suggested_suppliers_json"]
    #         }
    #     }
    #     return json.dumps(result, indent=4)
        

    def getAgent(self, llm):

        # tool = Tool(
        #     name="generate_summary",
        #     func=self.generate_summary,
        #     description="Provides a summary JSON combining weather conditions and suggested alternate suppliers.",
        # )

        # Create Agent
        agent = Agent(
            role="Summary Generator",
            goal="Create a JSON file from the json data suggested_suppliers and weather_condition",
            backstory="A json file generator",
            # tools=[tool],
            llm=llm,
            verbose=True,
        )

        return agent
    

    def getTask(self, agent, tasks):

        # Create Task
        task = Task(
            description=f"Create a JSON file from the json data suggested_suppliers and weather_condition",
            expected_output="A json file with the data suggested_suppliers and weather_condition",
            agent=agent,
            context=tasks,
            retries=0,  # Ensure no automatic retries
        )

        return task
    


    # def getAgent(self, llm):

    #     # Create Agent
    #     agent = Agent(
    #         name="Summary Agent",
    #         role="Combines JSON data and creates a summary",
    #         goal="Merge JSON data from both weather conditions and suggested alternate suppliers and generate a summary",
    #         llm=llm,
    #         verbose=True,
    #     )

    #     return agent
    

    # def getTask(self, agent, tasks):

    #     # Create Task
    #     task = Task(
    #         description=f"Create a JSON file from the json data suggested_suppliers and weather_condition",
    #         expected_output="A json file with the data suggested_suppliers and weather_condition",
    #         agent=agent,
    #         context=tasks,
    #         retries=0,  # Ensure no automatic retries
    #     )

    #     return task
    

