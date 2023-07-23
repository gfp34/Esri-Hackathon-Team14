from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from housing_data import HousingData
import utils

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data to store JSON messages
messages = []

@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        messages.append(data)
        return jsonify({"success": True, "message": "Message received successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/receive', methods=['GET'])
def receive_messages():
    housing_data = HousingData(True, False)
    housing_data.filter_by_cluster("Cluster 38")

    travel_mode = "walking"
    cutoff = [20]
    housing_data.sidebar_filter("Child_Care_Services_BA_Geocoded", travel_mode, cutoff)
    housing_data.sidebar_filter("Metro_Bus_Stops", travel_mode, cutoff)
    housing_data.sidebar_filter("wic_snap_points", travel_mode, cutoff)

    json_str = utils.layer_to_json_str(housing_data.public_layer_filter)

    return jsonify(json_str)

@app.route('/')
def index():
    return render_template('index.html')

def main():
    app.run(host='localhost', port=8080)
    

if __name__ == '__main__':
    main()
