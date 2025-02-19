from flask import Blueprint, request, render_template
import logging, os
import requests

from supply_control.SupplyControlMain import SupplyControlMain

apiSupplyControl = Blueprint('api_supply_control', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@apiSupplyControl.route('/api/supply_control/invoke', methods=['POST'])
def invoke_supply_control():
    logger.debug("/api/supply_control/invoke ...")

    payload = request.get_json()

    ### Call the main function to get the response
    supplyControlMain = SupplyControlMain()
    resp = supplyControlMain.invoke(payload)

    return resp, 200

# Route for the contact page
@apiSupplyControl.route('/supply_control')
def supply_control():
    order_number = request.args.get("order_number", "")  # Default is empty string if not provided
    location = request.args.get("location", "")

    # order_number = "1234"
    # delivery_location = "GGGGG"

    # Render the template with values
    return render_template("supply_control/supply.html", order_number=order_number, location=location)

# Route for supplier data 
@apiSupplyControl.route('/supplier_data')
def invoke_supplier_data():
    """Supplier page that shows API data in a table."""
    try:
        # Call the API to get data
        api_url = "http://127.0.0.1:3001/api/get-supplier-data"  # Update if needed
        response = requests.get(api_url)
        print("api response of supplier data = ",response)
        
        if response.status_code == 200:
            data = response.json()  # Convert JSON response to Python dict
        else:
            data = []  # If API fails, show empty data

    except Exception as e:
        data = []  # Handle any errors

    return render_template("supply_control/supply.html", data=data)