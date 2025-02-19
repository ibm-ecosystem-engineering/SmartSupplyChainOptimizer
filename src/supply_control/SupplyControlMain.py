import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool

from dotenv import load_dotenv
import json
import requests
import re

import logging

from llm.LlmMain import LlmMain
from util.DictionaryUtil import DictionaryUtil
from util.FileUtil import FileUtil
from supply_control.AgentWeather import AgentWeather
from supply_control.AgentSupplier import AgentSupplier
from supply_control.AgentDisruptionDetector import AgentDisruptionDetector
from supply_control.AgentSummary import AgentSummary
from CommonConstants import *

class SupplyControlMain(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self.fileUtil = FileUtil()
        self.fileUtil.start()

    def invoke(self, payload):
        self.logger.info("invoke started ... ")

        ### Retrive parameters
        location = payload["location"]
        supplier_file_name = "./data/Suppliers_Tennasse.csv"

        ### query watsonx model
        llmMain = LlmMain()
        model_id = "watsonx/ibm/granite-3-8b-instruct"
        llm = llmMain.get_watsonx_model_for_agents(model_id)

        # Agents and Tasks
        agentWeather = AgentWeather()
        weather_agent = agentWeather.getAgent(llm)
        weather_task = agentWeather.getTask(weather_agent, location)

        agentDisruptionDetector = AgentDisruptionDetector()
        disruption_detector_agent = agentDisruptionDetector.getAgent(llm)
        disruption_detector_task = agentDisruptionDetector.getTask(disruption_detector_agent, [weather_task])

        agentSupplier = AgentSupplier()
        supplier_agent = agentSupplier.getAgent(llm)
        supplier_task = agentSupplier.getTask(supplier_agent, [disruption_detector_task], supplier_file_name)

        agentSummary = AgentSummary()
        summary_agent = agentSummary.getAgent(llm)
        summary_task = agentSummary.getTask(summary_agent, [supplier_task])

        crew = Crew(
            agents=[
                weather_agent,
                disruption_detector_agent,
                supplier_agent,
                summary_agent
            ],
            tasks=[
                weather_task,
                disruption_detector_task,
                supplier_task,
                summary_task
            ],
            process=Process.sequential
        )

        #### Execute Crew
        crew_output = crew.kickoff()
        result_json = DictionaryUtil.getValue_key1(crew_output.dict(), "raw", None)
        result_json = re.sub(r"```json|```", "", result_json).strip()
        print("\nFinal Result 111:\n", result_json)

        #### Mock Output
        result_json = FileUtil.loadJsonAsObject("data/sample_output.json")

        resp = {
            "msg" : "Success",
            "result" : result_json
        }
        self.logger.info(f"Response : {resp} ")
        self.logger.info("invoke completed ... ")
        return resp