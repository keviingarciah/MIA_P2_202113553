from flask import Flask, jsonify, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, resources={r"/execute": {"origins": "http://localhost:5173"}})

# Respuesta de ejemplo
respuesta = {
    "mensaje": "[Success] => Backend levantado correctamente.",
}


# Ruta para obtener la lista de productos≠
@app.route("/", methods=["GET"])
def obtener_productos():
    return jsonify(respuesta)


# Ruta para ejecutar el código
@app.route("/execute", methods=["POST"])
def execute_code():
    # Obtener el mensaje enviado por el cliente
    data = request.get_json()

    #  Obtener script enviado por el cliente
    content = data.get("inputText", "")

    # print(content)

    # Aquí puedes ejecutar el código y obtener la salida
    output = content

    # Esperamos 1 segundo, para simular proceso de ejecución
    # time.sleep(1)

    return jsonify({"message": output})


if __name__ == "__main__":
    app.run(debug=True)
