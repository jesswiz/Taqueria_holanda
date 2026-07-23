from DOMAIN.entidades import Ingrediente

class IngredienteRepository:
    def __init__(self):
        # Datos ficticios
        self.ingredientes = {
            1: Ingrediente(id_ingrediente=1, nombre="Carne al Pastor", unidad_medida="kg"),
            2: Ingrediente(id_ingrediente=2, nombre="Tortilla de Maiz", unidad_medida="unidades"),
            3: Ingrediente(id_ingrediente=3, nombre="Cebolla", unidad_medida="kg"),
        }

    def obtener_todos(self):
        return list(self.ingredientes.values())

    def obtener_por_id(self, id_ingrediente):
        return self.ingredientes.get(id_ingrediente)

ingrediente_repository = IngredienteRepository()