from flask import Blueprint, jsonify, request

from DATA.pedido_repository import pedido_repository
from DATA.proveedor_repository import (
    proveedor_repository
)
from DOMAIN.servicio_pedido import (
    ConflictoPedidoError,
    DetalleNoEncontradoError,
    PedidoNoEncontradoError,
    ServicioPedido,
)


pedido_bp = Blueprint(
    "pedido_bp",
    __name__
)

servicio_pedido = ServicioPedido(
    pedido_repository=pedido_repository,
    proveedor_repository=proveedor_repository
)


def obtener_json_obligatorio():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        raise ValueError("Debe enviar un cuerpo JSON válido.")

    return datos


@pedido_bp.route(
    "/pedidos",
    methods=["GET"]
)
def listar_pedidos():
    pedidos = servicio_pedido.listar_pedidos()

    return jsonify({
        "mensaje": ("Pedidos obtenidos correctamente"),
        "pedidos": pedidos
    }), 200


@pedido_bp.route(
    "/pedidos/<int:id_pedido>",
    methods=["GET"]
)
def obtener_pedido(id_pedido):
    try:
        pedido = servicio_pedido.obtener_pedido(
            id_pedido
        )

        return jsonify({
            "mensaje": ("Pedido obtenido correctamente"),
            "pedido": pedido
        }), 200

    except PedidoNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404


@pedido_bp.route(
    "/pedidos",
    methods=["POST"]
)
def crear_pedido():
    try:
        datos = obtener_json_obligatorio()

        pedido = servicio_pedido.crear_pedido(
            id_pedido=datos["id_pedido"],
            id_proveedor=datos["id_proveedor"],
            id_sucursal=datos["id_sucursal"],
            fecha=datos["fecha"],
            estado=datos["estado"],
            detalles=datos["detalles"]
        )

        return jsonify({
            "mensaje": ("Pedido creado correctamente"),
            "pedido": pedido
        }), 201

    except KeyError as error:
        return jsonify({
            "error": (f"Falta el campo obligatorio:{error.args[0]}.")
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except ConflictoPedidoError as error:
        return jsonify({
            "error": str(error)
        }), 409


@pedido_bp.route(
    "/pedidos/<int:id_pedido>",
    methods=["PUT"]
)
def actualizar_pedido(id_pedido):
    try:
        datos = obtener_json_obligatorio()

        pedido = servicio_pedido.actualizar_pedido(
            id_pedido=id_pedido,
            id_proveedor=datos["id_proveedor"],
            id_sucursal=datos["id_sucursal"],
            fecha=datos["fecha"],
            estado=datos["estado"],
            detalles=datos["detalles"]
        )

        return jsonify({
            "mensaje": ("Pedido actualizado correctamente"),
            "pedido": pedido
        }), 200

    except KeyError as error:
        return jsonify({
            "error": (f"Falta el campo obligatorio: {error.args[0]}.")
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except PedidoNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404


@pedido_bp.route(
    "/pedidos/<int:id_pedido>",
    methods=["DELETE"]
)
def eliminar_pedido(id_pedido):
    try:
        pedido = servicio_pedido.eliminar_pedido(
            id_pedido
        )

        return jsonify({
            "mensaje": ("Pedido eliminado correctamente"),
            "pedido": pedido
        }), 200

    except PedidoNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404


@pedido_bp.route(
    "/pedidos/<int:id_pedido>/estado",
    methods=["PATCH"]
)
def cambiar_estado_pedido(id_pedido):
    try:
        datos = obtener_json_obligatorio()

        pedido = servicio_pedido.cambiar_estado(
            id_pedido=id_pedido,
            nuevo_estado=datos["estado"]
        )

        return jsonify({
            "mensaje": ("Estado del pedido actualizado correctamente"),
            "pedido": pedido
        }), 200

    except KeyError as error:
        return jsonify({
            "error": (f"Falta el campo obligatorio: {error.args[0]}.")
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except PedidoNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404


@pedido_bp.route(
    "/pedidos/<int:id_pedido>/detalles",
    methods=["POST"]
)
def agregar_detalle(id_pedido):
    try:
        datos = obtener_json_obligatorio()

        pedido = servicio_pedido.agregar_detalle(
            id_pedido=id_pedido,
            id_detalle=datos["id_detalle"],
            id_ingrediente=datos["id_ingrediente"],
            cantidad_pedido=datos["cantidad_pedido"]
        )

        return jsonify({
            "mensaje": ("Detalle agregado correctamente"),
            "pedido": pedido
        }), 201

    except KeyError as error:
        return jsonify({
            "error": (f"Falta el campo obligatorio: {error.args[0]}.")
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except PedidoNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404

    except ConflictoPedidoError as error:
        return jsonify({
            "error": str(error)
        }), 409


@pedido_bp.route(
    (
        "/pedidos/<int:id_pedido>/detalles/"
        "<int:id_detalle>"
    ),
    methods=["PUT"]
)
def actualizar_detalle(id_pedido, id_detalle):
    try:
        datos = obtener_json_obligatorio()

        pedido = servicio_pedido.actualizar_detalle(
            id_pedido=id_pedido,
            id_detalle=id_detalle,
            id_ingrediente=datos["id_ingrediente"],
            cantidad_pedido=datos["cantidad_pedido"]
        )

        return jsonify({
            "mensaje": ("Detalle actualizado correctamente"),
            "pedido": pedido
        }), 200

    except KeyError as error:
        return jsonify({
            "error": (f"Falta el campo obligatorio: {error.args[0]}.")
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except PedidoNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404

    except DetalleNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404


@pedido_bp.route(
    (
        "/pedidos/<int:id_pedido>/detalles/"
        "<int:id_detalle>"
    ),
    methods=["DELETE"]
)
def eliminar_detalle(id_pedido, id_detalle):
    try:
        pedido = servicio_pedido.eliminar_detalle(
            id_pedido=id_pedido,
            id_detalle=id_detalle
        )

        return jsonify({
            "mensaje": ("Detalle eliminado correctamente"),
            "pedido": pedido
        }), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except PedidoNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404

    except DetalleNoEncontradoError as error:
        return jsonify({
            "error": str(error)
        }), 404