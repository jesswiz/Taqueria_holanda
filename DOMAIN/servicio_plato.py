from DOMAIN.entidades import DetalleReceta, Plato
class PlatoNoEncontradoError(Exception):
    pass
class ConflictoPlatoError(Exception):
    pass

class ServicioPlato:
    def __init__(self, plato_repository, ingrediente_repository):
        self.plato_repository = plato_repository
        self.ingrediente_repository = ingrediente_repository
    def listar_platos(self):
        platos = self.plato_repository.obtener_todos()

        return [
            plato.convertir_a_diccionario()
            for plato in platos
        ]
    def obtener_plato(self, id_plato):
        plato = self._buscar_plato(id_plato)

        return plato.convertir_a_diccionario()
    def crear_plato(
        self,
        id_plato,
        nombre,
        descripcion,
        precio,
        receta
    ):
        plato_existente = self.plato_repository.obtener_por_id(id_plato)
        if plato_existente is not None:
            raise ConflictoPlatoError("Ya existe un plato con ese id.")
        detalles_receta = self._crear_detalles_receta(receta)
        plato = Plato(
            id_plato=id_plato,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio
        )
        for detalle in detalles_receta:
            plato.agregar_ingrediente(detalle)
        plato.validar_receta()
        self.plato_repository.agregar(plato)
        return plato.convertir_a_diccionario()

    def _buscar_plato(self, id_plato):
        plato = self.plato_repository.obtener_por_id(id_plato)
        if plato is None:
            raise PlatoNoEncontradoError("El plato no existe.")
        return plato

    def _crear_detalles_receta(self, receta):
        if not isinstance(receta, list):
            raise ValueError("La receta del plato debe enviarse en una lista.")
        if len(receta) == 0:
            raise ValueError("Un plato debe contener al menos un ingrediente en su receta.")

        detalles_creados = []
        for contador, datos_detalle in enumerate(receta, start=1):
            if not isinstance(datos_detalle, dict):
                raise ValueError("Cada ingrediente de la receta debe ser un objeto JSON.")
            try:
                id_ingrediente = datos_detalle["id_ingrediente"]
                cantidad_ingrediente = datos_detalle["cantidad_ingrediente"]
            except KeyError as error:
                raise ValueError(f"Falta el campo obligatorio: {error.args[0]}.") from error
            ingrediente = self.ingrediente_repository.obtener_por_id(id_ingrediente)
            if ingrediente is None:
                raise ValueError(f"No se puede registrar el plato porque el ingrediente {id_ingrediente} no existe.")
            detalle = DetalleReceta(
                id_detalle_receta=contador,
                id_ingrediente=id_ingrediente,
                cantidad_ingrediente=cantidad_ingrediente
            )
            detalles_creados.append(detalle)
        return detalles_creados