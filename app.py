import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from ROUTES.inventario_routes import inventario_bp
from ROUTES.pedido_routes import pedido_bp
from ROUTES.proveedor_routes import proveedor_bp
from ROUTES.plato_routes import plato_bp

from DOMAIN.servicio_proveedor import ProveedorNoEncontradoError, ConflictoProveedorError
from DOMAIN.servicio_pedido import PedidoNoEncontradoError, DetalleNoEncontradoError, ConflictoPedidoError
from DOMAIN.servicio_plato import PlatoNoEncontradoError, ConflictoPlatoError

load_dotenv()

app = Flask(__name__)

app.register_blueprint(inventario_bp)
app.register_blueprint(proveedor_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(plato_bp)

@app.errorhandler(ValueError)
def handle_value_error(error):
    
    return jsonify({"error": str(error)}), 400

@app.errorhandler(KeyError)
def handle_key_error(error):

    return jsonify({"error": f"Falta el campo obligatorio: {error.args[0]}."}), 400


@app.errorhandler(ProveedorNoEncontradoError)
@app.errorhandler(PedidoNoEncontradoError)
@app.errorhandler(DetalleNoEncontradoError)
@app.errorhandler(PlatoNoEncontradoError)
def handle_not_found_errors(error):
    return jsonify({"error": str(error)}), 404


@app.errorhandler(ConflictoProveedorError)
@app.errorhandler(ConflictoPedidoError)
@app.errorhandler(ConflictoPlatoError)
@app.errorhandler(RuntimeError)
def handle_conflict_errors(error):
    return jsonify({"error": str(error)}), 409



@app.route("/")
def inicio():
    return {
        "mensaje": (
            "API de Taquería Holanda "
            "funcionando correctamente"
        ),
        "capas": {
            "ROUTES": "Capa de presentación",
            "DOMAIN": (
                "Capa de lógica y reglas del negocio"
            ),
            "DATA": "Capa de datos"
        }
    }

if __name__ == "__main__":
    app.run(debug=True)