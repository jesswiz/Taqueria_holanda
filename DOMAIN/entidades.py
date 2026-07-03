from abc import ABC, abstractmethod

class Ingrediente:
    def __init__(self, id_ingrediente, nombre, unidad_medida):
        self.id_ingrediente = id_ingrediente
        self.nombre = nombre
        self.unidad_medida = unidad_medida

class Proveedor:
    def __init__(self, id_proveedor, nombre, telefono, direccion, DUI_nit):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.DUI_nit = DUI_nit

class Sucursal:
    def __init__(self, id_sucursal, nombre, direccion, ciudad, departamento, telefono):
        self.id_sucursal = id_sucursal
        self.nombre = nombre
        self.direccion = direccion
        self.ciudad = ciudad
        self.departamento = departamento
        self.telefono = telefono

class Inventario:
    def __init__(self, id_inventario, id_sucursal, id_ingrediente, cantidad_disponible):
        if cantidad_disponible < 0:
            raise ValueError("La cantidad disponible no puede ser negativa.")

        self.id_inventario = id_inventario
        self.id_sucursal = id_sucursal
        self.id_ingrediente = id_ingrediente
        self.cantidad_disponible = cantidad_disponible

    def convertir_a_diccionario(self):
        return {
            "id_inventario": self.id_inventario,
            "id_sucursal": self.id_sucursal,
            "id_ingrediente": self.id_ingrediente,
            "cantidad_disponible": self.cantidad_disponible
        }

class MovimientoInventario(ABC):
    def __init__(self, cantidad_movida, motivo):
        if cantidad_movida <= 0:
            raise ValueError("La cantidad movida debe ser mayor a cero.")

        self.cantidad_movida = cantidad_movida
        self.motivo = motivo

    @abstractmethod
    def aplicar_movimiento(self, inventario):
        pass
      
class EntradaInventario(MovimientoInventario):
    def aplicar_movimiento(self, inventario):
        inventario.cantidad_disponible += self.cantidad_movida
        return inventario

class SalidaInventario(MovimientoInventario):
    def aplicar_movimiento(self, inventario):
        if self.cantidad_movida > inventario.cantidad_disponible:
            raise RuntimeError("No se puede registrar salida: inventario insuficiente.")

        inventario.cantidad_disponible -= self.cantidad_movida
        return inventario
    
class DetallePedido:
    def __init__(self, id_ingrediente, cantidad_pedido):
        if cantidad_pedido <= 0:
            raise ValueError("La cantidad del pedido debe ser mayor a cero.")

        self.id_ingrediente = id_ingrediente
        self.cantidad_pedido = cantidad_pedido

    def convertir_a_diccionario(self):
        return {
            "id_ingrediente": self.id_ingrediente,
            "cantidad_pedido": self.cantidad_pedido
        }

class Pedido:
    def __init__(self, id_pedido, id_proveedor, id_sucursal, fecha, estado):
        self.id_pedido = id_pedido
        self.id_proveedor = id_proveedor
        self.id_sucursal = id_sucursal
        self.fecha = fecha
        self.estado = estado
        self._detalles = []

    @property
    def detalles(self):
        return tuple(self._detalles)

    def agregar_detalle(self, detalle):
        self._detalles.append(detalle)

    def validar_pedido(self):
        if len(self._detalles) == 0:
            raise ValueError("Un pedido debe contener al menos un detalle.")

    def convertir_a_diccionario(self):
        return {
            "id_pedido": self.id_pedido,
            "id_proveedor": self.id_proveedor,
            "id_sucursal": self.id_sucursal,
            "fecha": self.fecha,
            "estado": self.estado,
            "detalles": [detalle.convertir_a_diccionario() for detalle in self._detalles]
        }

class Plato:
    def __init__(self, id_plato, nombre, descripcion, precio):
        if precio <= 0:
            raise ValueError("El precio del plato debe ser mayor a cero.")

        self.id_plato = id_plato
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

class Receta:
    def __init__(self, id_receta, id_plato):
        self.id_receta = id_receta
        self.id_plato = id_plato
        self._ingredientes = []

    @property
    def ingredientes(self):
        return tuple(self._ingredientes)

    def agregar_ingrediente(self, id_ingrediente, cantidad_ingrediente):
        if cantidad_ingrediente <= 0:
            raise ValueError("La cantidad del ingrediente debe ser mayor a cero.")

        self._ingredientes.append({
            "id_ingrediente": id_ingrediente,
            "cantidad_ingrediente": cantidad_ingrediente
        })

    def validar_receta(self):
        if len(self._ingredientes) == 0:
            raise ValueError("Una receta debe tener al menos un ingrediente.")