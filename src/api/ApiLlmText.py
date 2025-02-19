from flask import Blueprint, request, render_template
import logging, os

from llm_text.LlmTextMain import LlmTextMain

apiLlmText = Blueprint('api_llm_text', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@apiLlmText.route('/api/text/invoke', methods=['POST'])
def invoke_text():
    logger.debug("/api/text/invoke ...")

    payload = request.get_json()

    ### Call the main function to get the response
    llmTextMain = LlmTextMain()
    resp = llmTextMain.invoke(payload)

    return resp, 200

@apiLlmText.route('/api/text/welcome', methods=['GET'])
def welcome_text():
    resp = {"msg" : "Welcome to Text LLM APIs"}
    return resp, 200

# Route for the contact page
@apiLlmText.route('/api/text/chat')
def chat():
    return render_template('chat.html')
