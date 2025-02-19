
from flask import Flask, request, jsonify, render_template, send_file
import logging
import os
from flask_cors import CORS

from dotenv import load_dotenv
from api.ApiLlmAgent import apiLlmAgent
from api.ApiLlmText import apiLlmText
from api.ApiMain import apiMain
from api.ApiGetData import getDataApi , getSupplierDataApi
from api.ApiSupplyControl import apiSupplyControl


# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enables CORS for all routes

# Load environment variables
load_dotenv()

#### Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(name)s : %(message)s',
    handlers=[
        logging.StreamHandler(),  # print to console
    ],
)
#### Log Init
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

### APIs
app.register_blueprint(apiMain)
app.register_blueprint(apiLlmText)
app.register_blueprint(apiLlmAgent)
app.register_blueprint(getDataApi)
app.register_blueprint(getSupplierDataApi)
app.register_blueprint(apiSupplyControl)

### Main method
def main():
    logger.info("main started .....")

    ### Run the app
    app.run(host ='0.0.0.0', port = 3001, debug = True)

### Invoke Main method
if __name__ == '__main__':
    main()