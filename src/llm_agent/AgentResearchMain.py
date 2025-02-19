import os
from crewai import Agent, Task, Crew
from langchain_ibm import WatsonxLLM
from dotenv import load_dotenv
import json

#### Here’s a simple CrewAI example using IBM Watsonx.ai LLM with two agents. Each agent independently calls the Watson LLM to process different tasks.

import logging

from llm.LlmMain import LlmMain
from util.DictionaryUtil import DictionaryUtil

from CommonConstants import *

class AgentResearchMain(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def invoke(self, payload):
        self.logger.info("invoke started ... ")

        ### Retrive parameters
        input = payload["input"]

        ### query watsonx model
        llmMain = LlmMain()
        model_id = "watsonx/ibm/granite-3-8b-instruct"
        watson_llm = llmMain.get_watsonx_model_for_agents(model_id)

        # 1️⃣ Research Agent - Fetches relevant information
        research_agent = Agent(
            role="Research Analyst",
            goal="Find detailed insights about the given topic",
            backstory="An AI-powered researcher that gathers knowledge efficiently.",
            verbose=True,
            llm=watson_llm
        )

        # 2️⃣ Summarization Agent - Summarizes the research
        summarization_agent = Agent(
            role="Content Summarizer",
            goal="Generate a concise summary of the research findings",
            backstory="An expert in distilling key points from complex information.",
            verbose=True,
            llm=watson_llm
        )

        # Define Tasks
        research_task = Task(
            description=f"Gather detailed insights about the topic: '{input}'",
            expected_output="A detailed response containing key information about the topic.",
            agent=research_agent
        )

        summary_task = Task(
            description="Summarize the research findings into a short paragraph",
            expected_output="A concise summary of the research findings.",
            agent=summarization_agent
        )

        # Create Crew
        crew = Crew(
            agents=[research_agent, summarization_agent],
            tasks=[research_task, summary_task],
            verbose=True
        )

        # Execute
        results = crew.kickoff()
        result_text = DictionaryUtil.getValue_key1(results.dict(), "raw", None)
        # json_string = json.dumps(results.dict())
        resp = {
            "msg" : "Success",
            "result" : result_text
        }
        print("\nFinal Summary:\n", results)

        self.logger.info("invoke completed ... ")

        return resp