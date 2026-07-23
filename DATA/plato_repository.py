from DOMAIN.entidades import Plato

class PlatoRepository:
    def __init__(self):
        self.platos = {}

    def obtener_todos(self):
        return list(self.platos.values())

    def obtener_por_id(self, id_plato):
        return self.platos.get(id_plato)

    def agregar(self, plato):
        if not isinstance(plato, Plato):
            raise ValueError("Solo se pueden guardar objetos Plato")

        self.platos[plato.id_plato] = plato
        return plato

plato_repository = PlatoRepository()