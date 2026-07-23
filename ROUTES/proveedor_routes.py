from flask import Blueprint, jsonify, request

from DATA.proveedor_repository import (
    proveedor_repository
)
from DOMAIN.servicio_proveedor import (
    ConflictoProveedorError,
    ProveedorNoEncontradoError,
    ServicioProveedor,
)


proveedor_bp = Blueprint(
    "proveedor_bp",
    __name__
)

servicio_proveedor = ServicioProveedor(
    proveedor_repository
)


def obtener_json_obligatorio():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        raise ValueError("Debe enviar un cuerpo JSON válido.")
    return datos


@proveedor_bp.route(
    "/proveedores",
    methods=["GET"]
)
def listar_proveedores():
    proveedores = (
        servicio_proveedor.listar_proveedores()
    )

    return jsonify({
        "mensaje": ("Proveedores obtenidos correctamente"),
        "proveedores": proveedores
    }), 200


@proveedor_bp.route(
    "/proveedores/<int:id_proveedor>",
    methods=["GET"]
)
def obtener_proveedor(id_proveedor):
    try:
        proveedor = (
            servicio_proveedor.obtener_proveedor(
                id_proveedor
            )
        )

        return jsonify({
            "mensaje": ("Proveedor obtenido correctamente"),
            "proveedor": proveedor
        }), 200

    except ProveedorNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404


@proveedor_bp.route(
    "/proveedores",
    methods=["POST"]
)
def crear_proveedor():
    try:
        datos = obtener_json_obligatorio()

        dui_nit = datos.get(
            "dui_nit",
            datos.get("DUI_nit")
        )

        proveedor = (
            servicio_proveedor.crear_proveedor(
                id_proveedor=datos["id_proveedor"],
                nombre=datos["nombre"],
                telefono=datos["telefono"],
                direccion=datos["direccion"],
                dui_nit=dui_nit
            )
        )

        return jsonify({
            "mensaje": ("Proveedor creado correctamente"),
            "proveedor": proveedor
        }), 201

    except KeyError as error:
        return jsonify({
            "error": (f"Falta el campo obligatorio:{error.args[0]}.")
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except ConflictoProveedorError as error:
        return jsonify({
            "error": str(error)
        }), 409


@proveedor_bp.route(
    "/proveedores/<int:id_proveedor>",
    methods=["PUT"]
)
def actualizar_proveedor(id_proveedor):
    try:
        datos = obtener_json_obligatorio()

        dui_nit = datos.get(
            "dui_nit",
            datos.get("DUI_nit")
        )

        proveedor = (
            servicio_proveedor.actualizar_proveedor(
                id_proveedor=id_proveedor,
                nombre=datos["nombre"],
                telefono=datos["telefono"],
                direccion=datos["direccion"],
                dui_nit=dui_nit
            )
        )

        return jsonify({
            "mensaje": ("Proveedor actualizado correctamente"),
            "proveedor": proveedor
        }), 200

    except KeyError as error:
        return jsonify({
            "error": (f"Falta el campo obligatorio: {error.args[0]}.")
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except ProveedorNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404

    except ConflictoProveedorError as error:
        return jsonify({
            "error": str(error)
        }), 409


@proveedor_bp.route(
    "/proveedores/<int:id_proveedor>",
    methods=["DELETE"]
)
def eliminar_proveedor(id_proveedor):
    try:
        proveedor = (
            servicio_proveedor.eliminar_proveedor(
                id_proveedor
            )
        )

        return jsonify({
            "mensaje": ("Proveedor eliminado correctamente"),
            "proveedor": proveedor
        }), 200

    except ProveedorNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404