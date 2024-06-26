from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from chat import invoke
import os
from load_data import load_data_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = 'data'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/query', methods=['POST'])
@cross_origin()
def query_handler():
    request_data = request.get_json()
    question = request_data.get('input', '')

    response = invoke(input=question)

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

        load_data_file(file_path)
        return jsonify({'response': 'Document uploaded and indexed successfully'})


if __name__ == '__main__':
    app.run(debug=True)
