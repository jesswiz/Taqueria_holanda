from flask import Flask, jsonify, request
from ROUTES.inventario_routes import inventario_bp

app = Flask(__name__)

app.register_blueprint(inventario_bp)

@app.route("/")
def inicio():
    return {
        "mensaje": "API de Taquería Holanda funcionando correctamente",
        "capas": {
            "ROUTES": "Capa de presentación",
            "DOMAIN": "Capa de lógica y reglas del negocio",
            "DATA": "Capa de datos"
        }
    }

if __name__ == "__main__":
    app.run(debug=True)


