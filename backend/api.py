

from flask import Flask, request, jsonify
from chat import invoke
from load_data import load_data

app = Flask(__name__)


@app.route('/query', methods=['POST'])
def query_handler():
    request_data = request.get_json()
    question = request_data.get('question', '')

    # gets the response from the retrieval_chain
    response = invoke(input=question)

    print('Results: ', response)

    # Rückgabe der Antwort im JSON-Format
    return jsonify({'response': response})


@app.route('/load_data', methods=['POST'])
def load_data_handler():
    request_data = request.get_json()
    data_path = request_data.get('data_path', '')

    # load data from the given data path
    load_data(data_path)

    return jsonify({'response': 'Data loaded successfully'})


if __name__ == '__main__':
    app.run(debug=True)
