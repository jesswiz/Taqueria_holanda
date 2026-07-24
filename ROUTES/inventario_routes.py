from flask import Blueprint, jsonify, request
from DATA.inventario_repository import inventario_repository
from DOMAIN.servicio_inventario import ServicioInventario

inventario_bp = Blueprint("inventario_bp", __name__)

servicio_inventario = ServicioInventario(inventario_repository)


def obtener_datos_json():
    return request.get_json(silent=True) or {}


def manejar_value_error(error):
    mensaje = str(error)

    if "no existe" in mensaje.lower():
        return jsonify({
            "error": mensaje
        }), 404

    return jsonify({
        "error": mensaje
    }), 400


@inventario_bp.route("/inventario", methods=["GET"])
def listar_inventario():
    inventario = servicio_inventario.listar_inventario()

    return jsonify({
        "mensaje": "Inventario obtenido correctamente",
        "inventario": inventario
    }), 200


@inventario_bp.route("/inventario/sucursal/<int:id_sucursal>", methods=["GET"])
def listar_inventario_por_sucursal(id_sucursal):
    try:
        inventario = (
            servicio_inventario.listar_inventario_por_sucursal(id_sucursal)
        )

        return jsonify({
            "mensaje": "Inventario de la sucursal obtenido correctamente",
            "inventario": inventario,
        }), 200

    except ValueError as error:
        return manejar_value_error(error)


@inventario_bp.route("/inventario/disponibilidad", methods=["POST"])
def comprobar_disponibilidad():
    try:
        datos = obtener_datos_json()

        disponibilidad = servicio_inventario.comprobar_disponibilidad(
            id_sucursal=datos.get("id_sucursal"),
            id_ingrediente=datos.get("id_ingrediente"),
            cantidad=datos.get("cantidad")
        )

        return jsonify({
            "mensaje": "Disponibilidad comprobada correctamente",
            "disponibilidad": disponibilidad
        }), 200

    except ValueError as error:
        return manejar_value_error(error)


@inventario_bp.route("/inventario/<int:id_inventario>/cantidad", methods=["PUT"])
def actualizar_cantidad(id_inventario):
    try:
        datos = obtener_datos_json()

        inventario_actualizado = (
            servicio_inventario.actualizar_cantidad(
                id_inventario=id_inventario,
                cantidad_disponible=datos.get("cantidad_disponible")
            )
        )

        return jsonify({
            "mensaje": "Cantidad disponible actualizada correctamente",
            "inventario": inventario_actualizado,
        }), 200

    except ValueError as error:
        return manejar_value_error(error)


@inventario_bp.route("/inventario/entrada", methods=["POST"])
def registrar_entrada():
    try:
        datos = obtener_datos_json()

        inventario_actualizado = servicio_inventario.registrar_entrada(
            id_inventario=datos.get("id_inventario"),
            cantidad=datos.get("cantidad"),
            motivo=datos.get("motivo")
        )

        return jsonify({
            "mensaje": "Entrada de inventario registrada correctamente",
            "inventario": inventario_actualizado
        }), 201

    except ValueError as error:
        return manejar_value_error(error)

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 409


@inventario_bp.route("/inventario/salida", methods=["POST"])
def registrar_salida():
    try:
        datos = obtener_datos_json()

        inventario_actualizado = servicio_inventario.registrar_salida(
            id_inventario=datos.get("id_inventario"),
            cantidad=datos.get("cantidad"),
            motivo=datos.get("motivo")
        )

        return jsonify({
            "mensaje": "Salida de inventario registrada correctamente",
            "inventario": inventario_actualizado
        }), 201

    except ValueError as error:
        return manejar_value_error(error)

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 409


@inventario_bp.route("/movimientos", methods=["POST"])
def registrar_movimiento():
    try:
        datos = obtener_datos_json()

        resultado = servicio_inventario.registrar_movimiento(
            id_inventario=datos.get("id_inventario"),
            tipo_accion=datos.get("tipo_accion"),
            cantidad_movida=datos.get("cantidad_movida"),
            fecha_accion=datos.get("fecha_accion"),
            motivo=datos.get("motivo")
        )

        return jsonify({
            "mensaje": "Movimiento de inventario aplicado correctamente",
            "inventario": resultado["inventario"],
            "movimiento": resultado["movimiento"]
        }), 201

    except ValueError as error:
        return manejar_value_error(error)

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 409


@inventario_bp.route("/movimientos", methods=["GET"])
def listar_movimientos():
    movimientos = servicio_inventario.listar_movimientos()

    return jsonify({
        "mensaje": "Movimientos obtenidos correctamente",
        "movimientos": movimientos
    }), 200


@inventario_bp.route("/inventario/<int:id_inventario>/movimientos", methods=["GET"])
def obtener_movimientos_por_inventario(id_inventario):
    try:
        movimientos = (
            servicio_inventario.obtener_movimientos_por_inventario(
                id_inventario
            )
        )

        return jsonify({
            "mensaje": "Movimientos del inventario obtenidos correctamente",
            "id_inventario": id_inventario,
            "movimientos": movimientos
        }), 200

    except ValueError as error:
        return manejar_value_error(error)