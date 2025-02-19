from flask import Blueprint, request, jsonify
import pandas as pd
import os

getDataApi = Blueprint('get_data_api', __name__)
getSupplierDataApi = Blueprint('get__supplier_data_api', __name__)

# Get absolute path of CSV file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_FILE_PATH = os.path.join(BASE_DIR, "data", "Orders.csv")
CSV_SUPPLIER_FILE_PATH = os.path.join(BASE_DIR, "data", "Suppliers_Tennasse.csv")


@getDataApi.route('/api/get-data', methods=['GET'])
def get_data():
    """API to return selected columns from a CSV file."""
    try:
        print("csv path = ", CSV_FILE_PATH)

        # Read CSV
        df = pd.read_csv(CSV_FILE_PATH)

        # Define static columns to return
        STATIC_COLUMNS = ["Order Number", "Source Location","Transit Location","Delivery Location", "Date ","Status","Supplier"]  # Change these to your actual column names

        # Validate columns exist in the CSV
        missing_columns = [col for col in STATIC_COLUMNS if col not in df.columns]
        if missing_columns:
            return jsonify({"error": f"Columns {missing_columns} not found in CSV"}), 400

        # Select and return only the static columns
        df_selected = df[STATIC_COLUMNS]
        return jsonify(df_selected.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@getSupplierDataApi.route('/api/get-supplier-data',methods=['GET'])
def get_supplier_data():
    """API to return selected columns from a CSV file."""
    try:
        print("csv path = ", CSV_SUPPLIER_FILE_PATH)

        # Read CSV
        df = pd.read_csv(CSV_SUPPLIER_FILE_PATH)

        # Define static columns to return
        STATIC_COLUMNS = ["SNo", "Category","SupplierName","City"]  # Change these to your actual column names

        # Validate columns exist in the CSV
        missing_columns = [col for col in STATIC_COLUMNS if col not in df.columns]
        if missing_columns:
            return jsonify({"error": f"Columns {missing_columns} not found in CSV"}), 400

        # Select and return only the static columns
        df_selected = df[STATIC_COLUMNS]
        return jsonify(df_selected.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
