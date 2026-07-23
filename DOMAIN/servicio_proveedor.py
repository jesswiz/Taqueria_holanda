from DOMAIN.entidades import Proveedor

class ProveedorNoEncontradoError(Exception):
    pass

class ConflictoProveedorError(Exception):
    pass

class ServicioProveedor:
    def __init__(self, proveedor_repository):
        self.proveedor_repository = proveedor_repository

    def listar_proveedores(self):
        proveedores = (self.proveedor_repository.obtener_todos())

        return [
            proveedor.convertir_a_diccionario()
            for proveedor in proveedores
        ]

    def obtener_proveedor(self, id_proveedor):
        proveedor = (
            self.proveedor_repository.obtener_por_id(
                id_proveedor
            )
        )

        if proveedor is None:
            raise ProveedorNoEncontradoError("El proveedor no existe.")

        return proveedor.convertir_a_diccionario()

    def crear_proveedor(
        self,
        id_proveedor,
        nombre,
        telefono,
        direccion,
        dui_nit
    ):
        proveedor_existente = (
            self.proveedor_repository.obtener_por_id(
                id_proveedor
            )
        )

        if proveedor_existente is not None:
            raise ConflictoProveedorError("Ya existe un proveedor con ese id.")

        dui_nit_normalizado = (
            dui_nit.strip()
            if isinstance(dui_nit, str)
            else dui_nit
        )

        proveedor_por_documento = (
            self.proveedor_repository.obtener_por_dui_nit(
                dui_nit_normalizado
            )
        )

        if proveedor_por_documento is not None:
            raise ConflictoProveedorError("Ya existe un proveedor con ese DUI o NIT.")

        proveedor = Proveedor(
            id_proveedor=id_proveedor,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            dui_nit=dui_nit_normalizado
        )

        self.proveedor_repository.agregar(proveedor)

        return proveedor.convertir_a_diccionario()

    def actualizar_proveedor(
        self,
        id_proveedor,
        nombre,
        telefono,
        direccion,
        dui_nit
    ):
        proveedor = (
            self.proveedor_repository.obtener_por_id(
                id_proveedor
            )
        )

        if proveedor is None:
            raise ProveedorNoEncontradoError("El proveedor no existe.")

        dui_nit_normalizado = (
            dui_nit.strip()
            if isinstance(dui_nit, str)
            else dui_nit
        )

        proveedor_con_mismo_documento = (
            self.proveedor_repository.obtener_por_dui_nit(
                dui_nit_normalizado
            )
        )

        if (
            proveedor_con_mismo_documento is not None
            and proveedor_con_mismo_documento.id_proveedor
            != id_proveedor
        ):
            raise ConflictoProveedorError("Ya existe otro proveedor con ese DUI o NIT.")

        proveedor_actualizado = Proveedor(
            id_proveedor=id_proveedor,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            dui_nit=dui_nit_normalizado
        )

        self.proveedor_repository.actualizar(
            proveedor_actualizado
        )

        return proveedor_actualizado.convertir_a_diccionario()

    def eliminar_proveedor(self, id_proveedor):
        proveedor = (
            self.proveedor_repository.eliminar(
                id_proveedor
            )
        )

        if proveedor is None:
            raise ProveedorNoEncontradoError("El proveedor no existe.")

        return proveedor.convertir_a_diccionario()