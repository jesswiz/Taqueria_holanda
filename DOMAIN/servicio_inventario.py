from datetime import date
from DOMAIN.entidades import MovimientoInventario

class ServicioInventario:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

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

    def actualizar_cantidad(
        self,
        id_inventario,
        cantidad_disponible
    ):
        inventario = (
            self.inventario_repository.obtener_por_id(
                id_inventario
            )
        )

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")

        inventario_actualizado = Inventario(
            id_inventario=inventario.id_inventario,
            id_sucursal=inventario.id_sucursal,
            id_ingrediente=inventario.id_ingrediente,
            cantidad_disponible=cantidad_disponible
        )

        self.inventario_repository.actualizar(inventario_actualizado)

        return (inventario_actualizado.convertir_a_diccionario())
        
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

        return resultado
    
