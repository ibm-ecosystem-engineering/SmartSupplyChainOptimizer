import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os

from llm.LlmMain import LlmMain

from CommonConstants import *

class LlmTextMain(object):

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
        question = payload["question"]

        ### query watsonx model
        llmMain = LlmMain()
        result = llmMain.invokeWatsonx_Text_model(question)
        resp = {
            "msg" : "Success",
            "result" : result
        }

        self.logger.info("invoke completed ... ")

        return resp