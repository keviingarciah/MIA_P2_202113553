# Libraries
from flask import Flask, jsonify, request
from flask_cors import CORS

# Modules
from analyzer import analyzer
from structs.user import Logged

# Global variables
CARNET = "53"

global mounted_partitions
mounted_partitions = {}

global logged
logged = Logged()


# Método para actualizar el mensaje
def update_message(new_message):
    global message
    message = new_message


# Backend
app = Flask(__name__)
CORS(app, resources={r"/execute": {"origins": "http://localhost:5173"}})


# Ruta para obtener el estado del backend
@app.route("/", methods=["GET"])
def corroborate():
    return jsonify({"message": "[Success] => Backend levantado correctamente."})


# Ruta para ejecutar el código
@app.route("/execute", methods=["POST"])
def execute_code():
    global message

    # Obtener el mensaje enviado por el cliente
    data = request.get_json()

    #  Obtener script enviado por el cliente
    script = data.get("inputText", "")

    # print(script)

    # Ejecutar el código
    message = analyzer.parse(script)

    return jsonify({"message": message})


# Main
if __name__ == "__main__":
    app.run(debug=True)
