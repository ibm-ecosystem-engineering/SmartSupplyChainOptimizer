import os, logging
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import json
from crewai_tools import ScrapeWebsiteTool
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from IPython.display import Markdown
from textwrap import dedent

from llm.LlmMain import LlmMain
from util.DictionaryUtil import DictionaryUtil
from CommonConstants import *

class AgentResearchPaperMain(object):

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
        model_id="watsonx/mistralai/mistral-large",
        model_id = "watsonx/ibm/granite-3-8b-instruct"
        llm = llmMain.get_watsonx_model_for_agents(model_id)


        # Define DuckDuckGo search as a proper tool
        search_tool = Tool(
            name="DuckDuckGo Search",
            func=lambda query: DuckDuckGoSearchRun().run(query),
            description="Searches the web for academic papers and research articles."
        )
        scrape_tool = ScrapeWebsiteTool()

        # Define Agents
        paper_finder = Agent(
            role='Research Paper Finder',
            goal='Find relevant scientific papers related to the input paper',
            backstory=("You are an expert at finding relevant scientific papers "
            "and research works. You use web search to discover papers that are closely "
            "related to a given research topic."),
            tools=[search_tool],
            llm=llm,
            verbose=True,
            allow_delegation=True
        )

        analyzer = Agent(
            role='Research Paper Analyst',
            goal='Analyze scientific papers to extract key knowledge and limitations',
            backstory=("You are an expert at analyzing scientific papers to identify "
            "key findings, methodologies, and limitations."),
            tools=[scrape_tool, search_tool],
            llm=llm,
            verbose=True,
            allow_delegation=True
        )

        seed_idea_generator = Agent(
            role='Seed Idea Generator',
            goal='Generate initial research ideas by combining knowledge from related papers',
            backstory=("You specialize in combining knowledge from multiple "
            "sources to generate novel research ideas."),
            tools=[search_tool],
            llm=llm,
            verbose=True,
            allow_delegation=True
        )

        idea_iterator = Agent(
            role='Idea Refinement Specialist',
            goal='Iterate and improve upon seed ideas',
            backstory=("You excel at taking initial research ideas and "
            "developing them through iteration and improvement."),
            tools=[search_tool],
            llm=llm,
            verbose=True,
            allow_delegation=True
        )

        completion_specialist = Agent(
            role='Research Proposal Developer',
            goal='Transform ideas into complete research proposals',
            backstory=("You are skilled at developing comprehensive research "
            "proposals with clear methodologies and experiment plans."),
            tools=[search_tool],
            llm=llm,
            verbose=True,
            allow_delegation=True
        )

        # Define Tasks
        paper_finding_task = Task(
            description="Find related scientific papers for the given input paper '{input_paper}' using web search.",
            expected_output="A JSON list of related papers including title, authors, and summary.",
            agent=paper_finder
        )

        analyze_papers_task = Task(
            description="Analyze the related papers to identify key knowledge and limitations.",
            expected_output="A JSON object summarizing key knowledge and limitations from the related papers.",
            agent=analyzer
        )

        seed_idea_generation_task = Task(
            description="Generate initial research ideas based on the knowledge and limitations provided in the analysis.",
            expected_output="A JSON list of research ideas including idea_title, description, and rationale.",
            agent=seed_idea_generator
        )

        idea_iteration_task = Task(
            description="Refine the generated seed ideas by expanding and identifying key improvements.",
            expected_output="A JSON list of refined ideas including refined_idea_title, description, and improvements.",
            agent=idea_iterator
        )

        completion_task = Task(
            description="Develop a complete research proposal based on the refined research ideas.",
            expected_output="A JSON list of research proposals including proposal_title, methodology, and experiment_plan.",
            agent=completion_specialist
        )

        # Create Crew
        scientific_crew = Crew(
            agents=[
                paper_finder,
                analyzer,
                seed_idea_generator,
                idea_iterator,
                completion_specialist
            ],
            tasks=[
                paper_finding_task,
                analyze_papers_task,
                seed_idea_generation_task,
                idea_iteration_task,
                completion_task
            ],
            process=Process.sequential
        )

        # Define Inputs
        inputs = {
            'input_paper': f"{input}"
        }

        # Execute the Crew
        results = scientific_crew.kickoff(inputs)
        result_text = DictionaryUtil.getValue_key1(results.dict(), "raw", None)
        # json_string = json.dumps(results.dict())
        resp = {
            "msg" : "Success",
            "result" : result_text
        }
        print("\nFinal Summary:\n", results)

        self.logger.info("invoke completed ... ")

        return resp