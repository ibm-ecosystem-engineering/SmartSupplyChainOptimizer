from flask import Blueprint, request, render_template
import logging, os
import requests

apiMain = Blueprint('api_main', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

# @apiMain.route('/')
# def index():
#     logger.info("main index page")
#     return render_template('index.html')

@apiMain.route('/')
def index():
    return render_template("index.html")

@apiMain.route('/order_control')
def order_control():
    """Home page that shows API data in a table."""
    try:
        # Call the API to get data
        api_url = "http://127.0.0.1:3001/api/get-data"  # Update if needed
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()  # Convert JSON response to Python dict
        else:
            data = []  # If API fails, show empty data

    except Exception as e:
        data = []  # Handle any errors

    return render_template("order_control.html", data=data)

@apiMain.route('/hello')
def hello():
    return "hello", 200

@apiMain.route('/welcome')
def welcome():
    return "Welcome to watxonx-ai Util application", 200

@apiMain.route('/about')
def about():
    return render_template('about.html')

# Route for the contact page
@apiMain.route('/contact')
def contact():
    return render_template('contact.html')
