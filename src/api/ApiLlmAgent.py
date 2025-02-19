from flask import Blueprint, request, render_template
import logging, os

from llm_agent.AgentResearchMain import AgentResearchMain
from llm_agent.AgentResearchPaperMain import AgentResearchPaperMain
from llm_agent.AgentWeatherMain import AgentWeatherMain

apiLlmAgent = Blueprint('api_llm_agent', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())


@apiLlmAgent.route('/api/agent/research', methods=['POST'])
def invoke_research():
    logger.debug("/api/agent/research ...")

    payload = request.get_json()

    ### Call the main function to get the response
    agentResearchMain = AgentResearchMain()
    resp = agentResearchMain.invoke(payload)

    return resp, 200

@apiLlmAgent.route('/api/agent/researchpaper', methods=['POST'])
def invoke_researchpaper():
    logger.debug("/api/agent/researchpaper ...")

    payload = request.get_json()

    ### Call the main function to get the response
    agentResearchPaperMain = AgentResearchPaperMain()
    resp = agentResearchPaperMain.invoke(payload)

    return resp, 200

@apiLlmAgent.route('/api/agent/weather', methods=['POST'])
def invoke_weather():
    logger.debug("/api/agent/weather ...")

    payload = request.get_json()

    ### Call the main function to get the response
    agentWeatherMain = AgentWeatherMain()
    resp = agentWeatherMain.invoke(payload)

    return resp, 200

@apiLlmAgent.route('/api/agent/welcome', methods=['GET'])
def welcome_text():
    resp = {"msg" : "Welcome to Agent LLM APIs"}
    return resp, 200

# Route for the contact page
@apiLlmAgent.route('/agent_research')
def agent_research():
    return render_template('agent_research.html')

# Route for the contact page
@apiLlmAgent.route('/agent_researchpaper')
def agent_researchpaper():
    return render_template('agent_researchpaper.html')

# Route for the contact page
@apiLlmAgent.route('/agent_weather')
def agent_weather():
    return render_template('agent_weather.html')



