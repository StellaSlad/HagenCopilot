"""
api.py

This module sets up a Flask web server to handle queries and document uploads.
It provides endpoints to process user queries using a language model and to upload and index documents.

Usage:
    Run this script directly to start the Flask web server.
"""

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from chat import invoke
import os
from load_data import load_data_file
from werkzeug.utils import secure_filename

# Load environment variables from a .env file
load_dotenv()

# Directory to store uploaded data and the model name
DATA_DIR = os.getenv("DATA_DIR")
MODEL = os.getenv("MODEL")

# Initialize the Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = DATA_DIR
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/query', methods=['POST'])
@cross_origin()
def query_handler():
    """
    Handle POST requests to the /query endpoint.

    This function processes the input query using the language model and returns the response.
    It expects a JSON payload with an 'input' field containing the user's question.

    Returns:
    Response: A JSON response containing the result of the query.
    """
    request_data = request.get_json()
    question = request_data.get('input', '')

    response = invoke(query=question, model=MODEL)

    print('Results: ', response)

    return response


@app.route('/upload_document', methods=['POST'])
@cross_origin()
def upload_document():
    """
    Handle POST requests to the /upload_document endpoint.

    This function uploads a document, saves it to the server, and indexes it.
    It expects a file part named 'document' in the request.

    Returns:
    Response: A JSON response indicating the success or failure of the upload and indexing process.
    """
    if 'document' not in request.files:
        return jsonify({'error': 'No document part'}), 400
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            load_data_file(file_path)
            # os.remove(file_path)  # Remove the file after processing
            return jsonify({'response': 'Document uploaded and indexed successfully'})
        except ValueError as e:
            # os.remove(file_path)  # Remove the file after processing
            print(e)
            return jsonify({'error': str(e)}), 409


if __name__ == "__main__":
    app.run(debug=True)
