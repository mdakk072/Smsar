import requests
import json
import sqlite3

base_url = 'http://127.0.0.1:5000'

table_name = 'Proprietes'

# Connect to the SQLite database
conn = sqlite3.connect('annonces.db')
cursor = conn.cursor()

# Execute the query to fetch all records from the annonces table
cursor.execute("SELECT * FROM annonces")
rows = cursor.fetchall()

# Iterate over each row
for row in rows:
    # Create a dictionary to hold the record data
    record = {
        'Type': row[1],
        'URLAnnonce': row[2],
        'Prix': row[4],
        'DatePublication': row[5],
        'Ville': row[6],
        'URLImage': row[7],
        'NombreImages': row[8]
    }

    # Use the POST method to add the record to the Proprietes table in the PostgreSQL database
    response = requests.post(f'{base_url}/add_record/{table_name}', json=record)
    print(response.json())  # Should print {'message': 'Record added.'} or {'message': 'Failed to add record.'}

# Close the connection to the SQLite database
conn.close()

# Test Update
update_data = {
    "filters": {"Type": "Villa"},
    "updates": {"Type": "Apartment"}
}
response = requests.put(f'{base_url}/update_record/{table_name}', json=update_data)
print(response.json())  # Should print {'message': 'X records updated.'} or {'message': 'Failed to update records.'}

# Test Delete
delete_data = {"Type": "Apartment"}
response = requests.delete(f'{base_url}/delete_record/{table_name}', json=delete_data)
print(response.json())  # Should print {'message': 'X records deleted.'} or {'message': 'Failed to delete records.'}

# Test Get
get_data = {"Type": "Villa"}
response = requests.get(f'{base_url}/get_record/{table_name}', params=get_data)
print(response.json())  # Should print the records or {'message': 'Failed to get records.'}
