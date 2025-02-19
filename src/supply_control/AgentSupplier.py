from datetime import datetime, timedelta
import logging
import os
from crewai import Agent, Task, Crew
from langchain.tools import Tool
from dotenv import load_dotenv

from util.FileUtil import FileUtil

### Static methods
class AgentSupplier :

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())


    def get_supplier_details(self, csv_file) :
        return FileUtil.csv_to_json(csv_file),

    def getAgent(self, llm):

        tool = Tool(
            name="get_supplier_details",
            func=self.get_supplier_details,
            description="Get the Suppliers details from CSV file",
        )

        # Create Agent
        agent = Agent(
            role="Supplier Provider",
            goal="List suppliers based in JSON format.",
            backstory="Suppliers expert who provides the right suppliers.",
            tools=[tool],
            llm=llm,
            verbose=True,
        )

        return agent
    

    def getTask(self, agent, tasks, csv_file_name):

        # Create Task
        task = Task(
            description=f"Retrieve suppliers from the csv file '{csv_file_name}'.",
            expected_output="list of suppliers including SNo,Category,Name in a json data with the key suggested_suppliers",
            agent=agent,
            context=tasks,
            retries=0,  # Ensure no automatic retries
        )
        return task
