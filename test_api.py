from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

data_dict = {}

@app.route('/', methods=['GET'])
def send_dict():
    return jsonify(data_dict)

@app.route('/api/receive_dict', methods=['POST'])
def receive_dict():
    data = request.get_json()  # Get the JSON data from the request
    with open('data.json', 'w') as f:
        json.dump(data, f)
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid data format. Expecting a dictionary.'}), 400

    # Update the data_dict with the received dictionary
    data_dict.update(data)

    return jsonify({'message': 'Dictionary received successfully.'}), 200
@app.route('/html_page', methods=['GET'])
def html_page():
    return render_template('index.html', data=data_dict)
if __name__ == '__main__':
    app.run(debug=True)
