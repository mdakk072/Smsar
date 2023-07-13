from flask import Flask, request, jsonify
from database import DatabaseManager

app = Flask(__name__)

db_manager = DatabaseManager('configDB.yaml')

@app.route('/add_record/<table_name>', methods=['POST'])
def add_record(table_name):
    # Extract data from the request.
    data = request.get_json()

    # Add the record to the database.
    if db_manager.add_record(table_name, **data):
        return jsonify(message='Record added.'), 201
    else:
        return jsonify(message='Failed to add record.'), 500

@app.route('/update_record/<table_name>', methods=['PUT'])
def update_record(table_name):
    # Extract data from the request.
    data = request.get_json()
    filters = data.get("filters")
    updates = data.get("updates")

    # Update the record in the database.
    count = db_manager.update_record(table_name, filters, **updates)
    if count is not None:
        return jsonify(message=f'{count} records updated.'), 200
    else:
        return jsonify(message='Failed to update records.'), 500


@app.route('/delete_record/<table_name>', methods=['DELETE'])
def delete_record(table_name):
    # Extract data from the request.
    data = request.get_json()

    # Delete the record from the database.
    count = db_manager.delete_records(table_name, data)
    if count is not None:
        return jsonify(message=f'{count} records deleted.'), 200
    else:
        return jsonify(message='Failed to delete records.'), 500

@app.route('/get_record/<table_name>', methods=['GET'])
def get_record(table_name):
    # Extract data from the request.
    data = request.args.to_dict()
    print(data)

    # Check if 'single' parameter is provided and if it is set to 'true'.

    # Get the records from the database.
    records = db_manager.get_records(table_name, **data)

    if records is not None:
        return jsonify(records=records), 200
    else:
        return jsonify(message='Failed to get records.'), 500


if __name__ == '__main__':
    app.run(debug=True)
