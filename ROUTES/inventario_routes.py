from flask import Blueprint, jsonify, request
from DATA.inventario_repository import InventarioRepository
from DOMAIN.servicio_inventario import ServicioInventario

inventario_bp = Blueprint("inventario_bp", __name__)

inventario_repository = InventarioRepository()
servicio_inventario = ServicioInventario(inventario_repository)


@inventario_bp.route("/inventario", methods=["GET"])
def listar_inventario():
    inventario = servicio_inventario.listar_inventario()

    return jsonify({
        "mensaje": "Inventario obtenido correctamente",
        "inventario": inventario
    })

@inventario_bp.route("/inventario/sucursal/<int:id_sucursal>", methods=["GET"])
def listar_inventario_por_sucursal(id_sucursal):
    try:
        inventario = (servicio_inventario.listar_inventario_por_sucursal(id_sucursal))

        return jsonify({
            "mensaje": (
                "Inventario de la sucursal obtenido correctamente"
            ),
            "inventario": inventario,
        })

@inventario_bp.route("/inventario/disponibilidad", methods=["POST"])
def comprobar_disponibilidad():
    try:
        datos = request.get_json()

        id_sucursal = datos["id_sucursal"]
        id_ingrediente = datos["id_ingrediente"]
        cantidad = datos["cantidad"]
        
        disponibilidad = (servicio_inventario.comprobar_disponibilidad(id_sucursal, id_ingrediente, cantidad))

        return jsonify({
            "mensaje": (
                "Disponibilidad comprobada correctamente"
            ),
            "disponibilidad": disponibilidad
        })
        
    except ValueError as error:
         return jsonify({
            "error": str(error)
        }), 400

@inventario_bp.route("/inventario/<int:id_inventario>/cantidad", methods=["PUT"])
def actualizar_cantidad(id_inventario):
    try:
         datos = request.get_json()

        cantidad_disponible = (
            datos["cantidad_disponible"]
        )

        inventario_actualizado = (servicio_inventario.actualizar_cantidad(id_inventario, cantidad_disponible))
        
        return jsonify({
            "mensaje": (
                "Cantidad disponible actualizada correctamente"
            ),
            "inventario": inventario_actualizado,
        })

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

@inventario_bp.route("/inventario/entrada", methods=["POST"])
def registrar_entrada():
    try:
        datos = request.get_json()

        id_inventario = datos["id_inventario"]
        cantidad = datos["cantidad"]
        motivo = datos["motivo"]

        inventario_actualizado = servicio_inventario.registrar_entrada(id_inventario, cantidad, motivo)

        return jsonify({
            "mensaje": "Entrada de inventario registrada correctamente",
            "inventario": inventario_actualizado
        })

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 409

@inventario_bp.route("/inventario/salida", methods=["POST"])
def registrar_salida():
    try:
        datos = request.get_json()

        id_inventario = datos["id_inventario"]
        cantidad = datos["cantidad"]
        motivo = datos["motivo"]

        inventario_actualizado = servicio_inventario.registrar_salida(
            id_inventario,
            cantidad,
            motivo
        )

        return jsonify({
            "mensaje": "Salida de inventario registrada correctamente",
            "inventario": inventario_actualizado
        })

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except RuntimeError as error:
        return jsonify({
            "error": str(error)
        }), 409
