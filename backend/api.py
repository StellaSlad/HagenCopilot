from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from chat import invoke
import os
from load_data import load_data_file
from werkzeug.utils import secure_filename


load_dotenv()

DATA_DIR = os.getenv("DATA_DIR")
MODEL = os.getenv("MODEL")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = DATA_DIR
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/query', methods=['POST'])
@cross_origin()
def query_handler():
    request_data = request.get_json()
    question = request_data.get('input', '')

    response = invoke(input=question, model=MODEL)

    print('Results: ', response)

    return response


@app.route('/upload_document', methods=['POST'])
@cross_origin()
def upload_document():
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
