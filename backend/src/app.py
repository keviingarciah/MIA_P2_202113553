# Libraries
from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from dotenv import load_dotenv
import os

# Modules
from main import logged
from analyzer import analyzer
from upload_report import reports


# Backend
app = Flask(__name__)
CORS(
    app,
    resources={
        r"/execute": {"origins": os.getenv("FRONTEND_URL")},
        r"/reports": {"origins": os.getenv("FRONTEND_URL")},
        r"/login": {"origins": os.getenv("FRONTEND_URL")},
        r"/session": {"origins": os.getenv("FRONTEND_URL")},
    },
)


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


# Ruta para login
@app.route("/login", methods=["POST"])
def login():
    # Obtener el mensaje enviado por el cliente
    data = request.get_json()

    # print(data)

    # Obtener los parámetros
    username = data.get("username", "")
    password = data.get("password", "")
    partitionId = data.get("id", "")

    """
    print(username)
    print(password)
    print(partitionId)
    """

    script = f"login -user={username} -pass={password} -id={partitionId}"

    # Iniciar sesión
    message = analyzer.parse(script)

    # print(message)

    return jsonify({"message": message})


# Ruta para obtener el estado de la sesión
@app.route("/session", methods=["GET"])
def get_session():
    # Se retorna el estado de la sesión
    return jsonify({"logged": logged.logged_in})


# Ruta para obtener reportes
@app.route("/reports", methods=["GET"])
def get_reports():
    # print(reports)

    # Se retornan los reportes
    return jsonify({"reports": reports})


# Main
if __name__ == "__main__":
    app.run(debug=True)
