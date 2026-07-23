from datetime import date
from DOMAIN.entidades import MovimientoInventario

class ServicioInventario:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    @staticmethod
    def _validar_id(valor, nombre):
        if (
            not isinstance(valor, int)
            or isinstance(valor, bool)
            or valor <= 0
        ):
            raise ValueError(f"{nombre} debe ser un número entero mayor a cero.")

    @staticmethod
    def _validar_cantidad(cantidad, permitir_cero=False):
        if (
            not isinstance(cantidad, (int, float))
            or isinstance(cantidad, bool)
        ):
            raise ValueError("La cantidad debe ser numérica.")
        if permitir_cero:
            if cantidad < 0:
                raise ValueError("La cantidad disponible no puede ser negativa.")
        elif cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

    @staticmethod
    def _validar_motivo(motivo):
        if not isinstance(motivo, str) or motivo.strip() == "":
            raise ValueError("El movimiento debe tener un motivo.")
            
    def _obtener_inventario(self, id_inventario):
        self._validar_id(id_inventario, "El id del inventario")

        inventario = self.inventario_repository.obtener_por_id(id_inventario)

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")

        return inventario

    def listar_inventario(self):
        inventarios = self.inventario_repository.obtener_todos()

        return [inventario.convertir_a_diccionario() for inventario in inventarios]
        
    def listar_inventario_por_sucursal(self, id_sucursal):
        self._validar_id(id_sucursal, "El id de la sucursal")

        inventarios = (self.inventario_repository.obtener_por_sucursal(id_sucursal))

        return [
            inventario.convertir_a_diccionario()
            for inventario in inventarios
        ]

    def comprobar_disponibilidad(self, id_sucursal, id_ingrediente, cantidad):
        self._validar_id(id_sucursal, "El id de la sucursal")

        self._validar_id(id_ingrediente, "El id del ingrediente")

        self._validar_cantidad(cantidad)
        inventario = (
            self.inventario_repository.obtener_por_sucursal_e_ingrediente(id_sucursal, id_ingrediente)
        )

        if inventario is None:
            raise ValueError("No existe inventario para ese ingrediente en la sucursal indicada.")
         
        return {
            "id_inventario": inventario.id_inventario,
            "id_sucursal": inventario.id_sucursal,
            "id_ingrediente": inventario.id_ingrediente,
            "cantidad_solicitada": cantidad,
            "cantidad_disponible": (
                inventario.cantidad_disponible
            ),
            "hay_suficiente": inventario.hay_suficiente(
                cantidad
            ),
        }

    def registrar_entrada(self, id_inventario, cantidad, motivo):
        inventario = self.inventario_repository.obtener_por_id(id_inventario)
        
        self._validar_cantidad(cantidad)
        self._validar_motivo(motivo)

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")}

        movimiento = MovimientoInventario(
            tipo_accion="entrada",
            cantidad_movida=cantidad,
            fecha_accion=str(date.today()),
            motivo=motivo
        )

        inventario_actualizado = movimiento.aplicar_movimiento(inventario)

        self.inventario_repository.actualizar(inventario_actualizado)

        return inventario_actualizado.convertir_a_diccionario()

    def registrar_salida(self, id_inventario, cantidad, motivo):
        
        inventario = self.inventario_repository.obtener_por_id(id_inventario)

        self._validar_cantidad(cantidad)
        self._validar_motivo(motivo)

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")

        movimiento = MovimientoInventario(
            tipo_accion="salida",
            cantidad_movida=cantidad,
            fecha_accion=str(date.today()),
            motivo=motivo
        )

        inventario_actualizado = movimiento.aplicar_movimiento(inventario)

        self.inventario_repository.actualizar(inventario_actualizado)

        return inventario_actualizado.convertir_a_diccionario()

    def actualizar_cantidad_disponible(self, id_inventario, nueva_cantidad, motivo):
        
        inventario = self._obtener_inventario(id_inventario)

        self._validar_cantidad(nueva_cantidad, permitir_cero=True)
        self._validar_motivo(motivo)

        cantidad_anterior = inventario.cantidad_disponible
        diferencia = nueva_cantidad - cantidad_anterior
        
        if diferencia > 0:
            movimiento = MovimientoInventario(
                tipo_accion="entrada",
                cantidad_movida=diferencia,
                fecha_accion=str(date.today()),
                motivo=motivo.strip(),
            )

            movimiento.aplicar_movimiento(inventario)

        elif diferencia < 0:
            movimiento = MovimientoInventario(
                tipo_accion="salida",
                cantidad_movida=abs(diferencia),
                fecha_accion=str(date.today()),
                motivo=motivo.strip(),
            )

            movimiento.aplicar_movimiento(inventario)
        
        self.inventario_repository.actualizar(inventario)

        resultado = inventario.convertir_a_diccionario()

        resultado["cantidad_anterior"] = cantidad_anterior
        resultado["cantidad_actual"] = (inventario.cantidad_disponible)

        return resultado
    
