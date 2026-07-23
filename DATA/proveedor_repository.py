from DOMAIN.entidades import Proveedor
class ProveedorRepository:
    def __init__(self):
        self.proveedores = {}

    def obtener_todos(self):
        return list(self.proveedores.values())

    def obtener_por_id(self, id_proveedor):
        return self.proveedores.get(id_proveedor)

    def obtener_por_dui_nit(self, dui_nit):
        return next(
            (
                proveedor
                for proveedor in self.proveedores.values()
                if proveedor.dui_nit == dui_nit
            ),
            None
        )

    def agregar(self, proveedor):
        if not isinstance(proveedor, Proveedor):
            raise ValueError("Solo se pueden guardar objetos Proveedor.")

        self.proveedores[proveedor.id_proveedor] = proveedor
        return proveedor

    def actualizar(self, proveedor):
        if not isinstance(proveedor, Proveedor):
            raise ValueError("Solo se pueden actualizar objetos Proveedor.")

        self.proveedores[proveedor.id_proveedor] = proveedor
        return proveedor

    def eliminar(self, id_proveedor):
        return self.proveedores.pop(id_proveedor, None)

proveedor_repository = ProveedorRepository()