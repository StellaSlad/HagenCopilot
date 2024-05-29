

from flask import Flask, request, jsonify
import subprocess
import sys
import time
import json

app = Flask(__name__)

# Variable, um zu überprüfen, ob Docker-Compose und load_data.py bereits gestartet wurden
services_started = False


#Funktion zum Starten der Docker-Compose
def start_docker_compose(compose_file):
    try:
        subprocess.run(['docker-compose', '-f', compose_file, 'up', '-d'], check=True)
        print("Docker-Compose gestartet.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Starten von Docker-Compose: {e}")
        sys.exit(1)

# Funktion zum Starten der chat.py
def start_chat_file(chat_file, data):
    try:
        input_data = json.dumps(data)
        result = subprocess.run(
            [sys.executable, chat_file],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
        output = result.stdout.strip()
        return output
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Starten der Python-Datei: {e}")
        sys.exit(1)


# Funktion zum Starten der load_data.py
def start_load_file(load_file):
    try:
        subprocess.Popen([sys.executable, load_file])
        print(f"{load_file} gestartet.")
    except Exception as e:
        print(f"Fehler beim Starten der Python-Datei: {e}")
        sys.exit(1)

@app.route('/query', methods=['POST'])
def query_handler():
        request_data = request.get_json()
        question = request_data.get('question', '')
        
        
        # Übergibt die Keywords an chat.py und erhält das Ergebnis
        response = start_chat_file('chat.py', question)
        
        print('Results: ', response)

        
        # Rückgabe der Antwort im JSON-Format 
        return jsonify({'response': response})
    

if __name__ == '__main__':
    #Docker-Compose starten
    start_docker_compose('docker-compose.yml')
    
    #Pause, damit Dienste sicher gestartet sind
    time.sleep(5)
    
    #load_data.py starten
    start_load_file('load_data.py')
    
    app.run(debug=True)
    
    
