from DOMAIN.entidades import EntradaInventario, SalidaInventario

class ServicioInventario:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def listar_inventario(self):
        inventarios = self.inventario_repository.obtener_todos()

        return [inventario.convertir_a_diccionario() for inventario in inventarios]

    def registrar_entrada(self, id_inventario, cantidad, motivo):
        inventario = self.inventario_repository.obtener_por_id(id_inventario)

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")

        movimiento = EntradaInventario(cantidad, motivo)
        inventario_actualizado = movimiento.aplicar_movimiento(inventario)

        self.inventario_repository.actualizar(inventario_actualizado)

        return inventario_actualizado.convertir_a_diccionario()

    def registrar_salida(self, id_inventario, cantidad, motivo):
        inventario = self.inventario_repository.obtener_por_id(id_inventario)

        if inventario is None:
            raise ValueError("El registro de inventario no existe.")

        movimiento = SalidaInventario(cantidad, motivo)
        inventario_actualizado = movimiento.aplicar_movimiento(inventario)

        self.inventario_repository.actualizar(inventario_actualizado)

        return inventario_actualizado.convertir_a_diccionario()
    