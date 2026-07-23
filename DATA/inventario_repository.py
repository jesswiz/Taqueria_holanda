from DOMAIN.entidades import Inventario

class InventarioRepository:

    def __init__(self):

        # Datos ficticios para desarrollo local sin base de datos
        self.inventarios = {
            1: Inventario(
                id_inventario=1,
                id_sucursal=1,
                id_ingrediente=1,
                cantidad_disponible=50,
            ),
            2: Inventario(
                id_inventario=2,
                id_sucursal=1,
                id_ingrediente=2,
                cantidad_disponible=30,
            ),
            3: Inventario(
                id_inventario=3,
                id_sucursal=2,
                id_ingrediente=3,
                cantidad_disponible=20,
            ),
        }

    def obtener_todos(self):
        return list(self.inventarios.values())

    def obtener_por_id(self, id_inventario):
        return self.inventarios.get(id_inventario)

    def actualizar(self, inventario):
        self.inventarios[inventario.id_inventario] = inventario
inventario_repository = InventarioRepository()
