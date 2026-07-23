from flask import Blueprint, jsonify, request
from DATA.ingrediente_repository import ingrediente_repository
from DATA.plato_repository import plato_repository
from DOMAIN.servicio_plato import (
    ConflictoPlatoError,
    PlatoNoEncontradoError,
    ServicioPlato,
)

plato_bp = Blueprint(
    "plato_bp",__name__)

servicio_plato = ServicioPlato(
    plato_repository=plato_repository,
    ingrediente_repository=ingrediente_repository)

def obtener_json_obligatorio():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        raise ValueError("Debe enviar un cuerpo JSON válido.")
    return datos

@plato_bp.route(
    "/platos",
    methods=["GET"])

def listar_platos():
    platos = servicio_plato.listar_platos()
    return jsonify({
        "mensaje": "Platos obtenidos correctamente",
        "platos": platos
    }), 200


@plato_bp.route(
    "/platos/<int:id_plato>",
    methods=["GET"])

def obtener_plato(id_plato):
    try:
        plato = servicio_plato.obtener_plato(id_plato)

        return jsonify({
            "mensaje": "Plato obtenido correctamente",
            "plato": plato
        }), 200
    except PlatoNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404

@plato_bp.route(
    "/platos",
    methods=["POST"]
)
def crear_plato():
    try:
        datos = obtener_json_obligatorio()
        plato = servicio_plato.crear_plato(
            id_plato=datos["id_plato"],
            nombre=datos["nombre"],
            descripcion=datos["descripcion"],
            precio=datos["precio"],
            receta=datos["receta"]
        )
        return jsonify({
            "mensaje": "Plato creado correctamente",
            "plato": plato
        }), 201
    
    except KeyError as error:
        return jsonify({
            "error": f"Falta el campo obligatorio: {error.args[0]}."
        }), 400
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
    except ConflictoPlatoError as error:
        return jsonify({
            "error": str(error)
        }), 409