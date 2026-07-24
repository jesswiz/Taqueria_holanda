from datetime import date
from DOMAIN.entidades import MovimientoInventario


class ServicioInventario:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def listar_inventario(self):
        inventarios = self.inventario_repository.obtener_todos()

        return [
            inventario.convertir_a_diccionario()
            for inventario in inventarios
        ]

    def listar_inventario_por_sucursal(self, id_sucursal):
        self._validar_id(id_sucursal, "El id de la sucursal")

        inventarios = (
            self.inventario_repository.obtener_por_sucursal(id_sucursal)
        )

        return [
            inventario.convertir_a_diccionario()
            for inventario in inventarios
        ]

    def comprobar_disponibilidad(
        self,
        id_sucursal,
        id_ingrediente,
        cantidad
    ):
        self._validar_id(id_sucursal, "El id de la sucursal")
        self._validar_id(id_ingrediente, "El id del ingrediente")
        self._validar_cantidad(cantidad)

        inventario = (
            self.inventario_repository.obtener_por_sucursal_e_ingrediente(
                id_sucursal,
                id_ingrediente
            )
        )

        if inventario is None:
            raise ValueError(
                "No existe inventario para ese ingrediente en la sucursal indicada."
            )

        return {
            "id_inventario": inventario.id_inventario,
            "id_sucursal": inventario.id_sucursal,
            "id_ingrediente": inventario.id_ingrediente,
            "cantidad_solicitada": cantidad,
            "cantidad_disponible": inventario.cantidad_disponible,
            "hay_suficiente": inventario.hay_suficiente(cantidad),
        }

    def actualizar_cantidad(
        self,
        id_inventario,
        cantidad_disponible
    ):
        self._validar_id(id_inventario, "El id del inventario")
        self._validar_cantidad_no_negativa(cantidad_disponible)

        inventario = (
            self.inventario_repository.obtener_por_id(id_inventario)
        )

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")

        inventario.cantidad_disponible = cantidad_disponible

        self.inventario_repository.actualizar(inventario)

        return inventario.convertir_a_diccionario()

    def registrar_entrada(self, id_inventario, cantidad, motivo):
        resultado = self.registrar_movimiento(
            id_inventario=id_inventario,
            tipo_accion="entrada",
            cantidad_movida=cantidad,
            motivo=motivo
        )

        return resultado["inventario"]

    def registrar_salida(self, id_inventario, cantidad, motivo):
        resultado = self.registrar_movimiento(
            id_inventario=id_inventario,
            tipo_accion="salida",
            cantidad_movida=cantidad,
            motivo=motivo
        )

        return resultado["inventario"]

    def registrar_movimiento(
        self,
        id_inventario,
        tipo_accion,
        cantidad_movida,
        motivo,
        fecha_accion=None
    ):
        self._validar_id(id_inventario, "El id del inventario")

        inventario = (
            self.inventario_repository.obtener_por_id(id_inventario)
        )

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")

        fecha = fecha_accion if fecha_accion is not None else str(date.today())

        movimiento = MovimientoInventario(
            id_inventario=id_inventario,
            tipo_accion=tipo_accion,
            cantidad_movida=cantidad_movida,
            fecha_accion=fecha,
            motivo=motivo
        )

        inventario_actualizado = movimiento.aplicar_movimiento(inventario)

        self.inventario_repository.actualizar(inventario_actualizado)

        return {
            "inventario": inventario_actualizado.convertir_a_diccionario(),
            "movimiento": movimiento.convertir_a_diccionario()
        }

    def obtener_movimientos_por_inventario(self, id_inventario):
        self._validar_id(id_inventario, "El id del inventario")

        inventario = (
            self.inventario_repository.obtener_por_id(id_inventario)
        )

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")

        return [
            movimiento.convertir_a_diccionario()
            for movimiento in inventario.movimientos
        ]

    def listar_movimientos(self):
        inventarios = self.inventario_repository.obtener_todos()
        movimientos = []

        for inventario in inventarios:
            for movimiento in inventario.movimientos:
                datos_movimiento = movimiento.convertir_a_diccionario()
                datos_movimiento["id_inventario"] = inventario.id_inventario
                movimientos.append(datos_movimiento)

        return movimientos

    def _validar_id(self, valor, nombre_campo):
        if (
            not isinstance(valor, int)
            or isinstance(valor, bool)
            or valor <= 0
        ):
            raise ValueError(f"{nombre_campo} debe ser un número entero mayor a cero.")

    def _validar_cantidad(self, cantidad):
        if (
            not isinstance(cantidad, (int, float))
            or isinstance(cantidad, bool)
        ):
            raise ValueError("La cantidad debe ser numérica.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

    def _validar_cantidad_no_negativa(self, cantidad):
        if (
            not isinstance(cantidad, (int, float))
            or isinstance(cantidad, bool)
        ):
            raise ValueError("La cantidad disponible debe ser numérica.")

        if cantidad < 0:
            raise ValueError("La cantidad disponible no puede ser negativa.")

    def _validar_motivo(self, motivo):
        if not isinstance(motivo, str) or motivo.strip() == "":
            raise ValueError("El motivo del movimiento es obligatorio.")