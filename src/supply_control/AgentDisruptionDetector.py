import os
from crewai import Agent, Task, Crew
from langchain.tools import Tool

from dotenv import load_dotenv
import json
import requests

#### Here’s a simple CrewAI example using IBM Watsonx.ai LLM with two agents. Each agent independently calls the Watson LLM to process different tasks.

import logging

from llm.LlmMain import LlmMain
from util.CommonUtil import CommonUtil

from CommonConstants import *

class AgentDisruptionDetector(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

        
    def detect_disruption(self, temperature, humidity, wind_speed):
        temperature = CommonUtil.str_to_float(temperature, 0)
        humidity = CommonUtil.str_to_float(humidity, 0)
        temperature = CommonUtil.str_to_float(wind_speed, 0)

        disruption_risk = temperature > 35 and humidity < 30 and wind_speed > 40
        return "High supply disruption risk detected! Immediate action required." if disruption_risk else "supply disruption risk is low."

    def getAgent(self, llm):

        tool = Tool(
            name="detect_disruption",
            func=self.detect_disruption,
            description="Detect the supply disruption based on the given temperature, wind_speed, humidity",
        )

        # Create Agent
        agent = Agent(
            role="supply disruption Risk Detector",
            goal="Analyze weather conditions and detect supply disruption",
            backstory="An expert in weather behavior who assesses supply disruption risks based on temperature, humidity, and wind speed.",
            tools=[tool],
            llm=llm,
            verbose=True,
        )

        return agent
    

    def getTask(self, agent, tasks):

        # Create Task
        task = Task(
            description=f"Analyze weather conditions and determine supply disruption risk.",
            expected_output="supply disruption risk assessment.",
            agent=agent,
            context=tasks,
            retries=0,
        )

        return task