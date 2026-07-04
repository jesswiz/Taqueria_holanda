class Ingrediente:
    def __init__(self, id_ingrediente, nombre, unidad_medida):
        self.id_ingrediente = id_ingrediente
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.validar_ingrediente()

    def validar_ingrediente(self):
        if self.id_ingrediente is None:
            raise ValueError("El ingrediente debe tener un id.")

        if self.nombre == "":
            raise ValueError("El ingrediente debe tener nombre.")

        if self.unidad_medida == "":
            raise ValueError("El ingrediente debe tener unidad de medida.")

class Proveedor:
    def __init__(self, id_proveedor, nombre, telefono, direccion, DUI_nit):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.DUI_nit = DUI_nit
        self.validar_proveedor()

    def validar_proveedor(self):
        if self.id_proveedor is None:
            raise ValueError("El proveedor debe tener un id.")

        if self.nombre == "":
            raise ValueError("El proveedor debe tener nombre.")

        if self.telefono == "":
            raise ValueError("El proveedor debe tener teléfono.")

        if self.direccion == "":
            raise ValueError("El proveedor debe tener dirección.")

        if self.DUI_nit == "":
            raise ValueError("El proveedor debe tener DUI o NIT.")

class Sucursal:
    def __init__(self, id_sucursal, nombre, direccion, ciudad, departamento, telefono):
        self.id_sucursal = id_sucursal
        self.nombre = nombre
        self.direccion = direccion
        self.ciudad = ciudad
        self.departamento = departamento
        self.telefono = telefono
        self.validar_sucursal()

    def validar_sucursal(self):
        if self.id_sucursal is None:
            raise ValueError("La sucursal debe tener un id.")

        if self.nombre == "":
            raise ValueError("La sucursal debe tener nombre.")

        if self.direccion == "":
            raise ValueError("La sucursal debe tener dirección.")

        if self.ciudad == "":
            raise ValueError("La sucursal debe tener ciudad.")

        if self.departamento == "":
            raise ValueError("La sucursal debe tener departamento.")

        if self.telefono == "":
            raise ValueError("La sucursal debe tener teléfono.")

class Inventario:
    def __init__(self, id_inventario, id_sucursal, id_ingrediente, cantidad_disponible):
        if id_inventario is None:
            raise ValueError("El inventario debe tener un id.")

        if id_sucursal is None:
            raise ValueError("El inventario debe estar asociado a una sucursal.")

        if id_ingrediente is None:
            raise ValueError("El inventario debe estar asociado a un ingrediente.")

        if cantidad_disponible < 0:
            raise ValueError("La cantidad disponible no puede ser negativa.")
        
        self.id_inventario = id_inventario
        self.id_sucursal = id_sucursal
        self.id_ingrediente = id_ingrediente
        self.cantidad_disponible = cantidad_disponible
        self._movimientos = []

    @property
    def movimientos(self):
        return tuple(self._movimientos)

    def aumentar_cantidad(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a aumentar debe ser mayor a cero.")

        self.cantidad_disponible += cantidad

    def disminuir_cantidad(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a disminuir debe ser mayor a cero.")

        if not self.hay_suficiente(cantidad):
            raise RuntimeError("No se puede registrar salida: inventario insuficiente.")

        self.cantidad_disponible -= cantidad

    def hay_suficiente(self, cantidad):
        return self.cantidad_disponible >= cantidad

    def registrar_movimiento(self, movimiento):
        self._movimientos.append(movimiento)

    def convertir_a_diccionario(self):
        return {
            "id_inventario": self.id_inventario,
            "id_sucursal": self.id_sucursal,
            "id_ingrediente": self.id_ingrediente,
            "cantidad_disponible": self.cantidad_disponible,
            "movimientos": [ movimiento.convertir_a_diccionario()
            for movimiento in self._movimientos]
        }

class MovimientoInventario:
    def __init__(self, tipo_accion, cantidad_movida, fecha_accion, motivo):
        self.tipo_accion = tipo_accion
        self.cantidad_movida = cantidad_movida
        self.fecha_accion = fecha_accion
        self.motivo = motivo

        self.validar_movimiento()

    def validar_movimiento(self):
        if self.tipo_accion not in ["entrada", "salida"]:
            raise ValueError("El tipo de acción debe ser entrada o salida.")

        if self.cantidad_movida <= 0:
            raise ValueError("La cantidad movida debe ser mayor a cero.")

        if self.fecha_accion == "":
            raise ValueError("El movimiento debe tener fecha.")

        if self.motivo == "":
            raise ValueError("El movimiento debe tener motivo.")

    def aplicar_movimiento(self, inventario):
        if self.tipo_accion == "entrada":
            inventario.aumentar_cantidad(self.cantidad_movida)

        elif self.tipo_accion == "salida":
            inventario.disminuir_cantidad(self.cantidad_movida)

        inventario.registrar_movimiento(self)
        return inventario
    
    def convertir_a_diccionario(self):
        return {
            "tipo_accion": self.tipo_accion,
            "cantidad_movida": self.cantidad_movida,
            "fecha_accion": self.fecha_accion,
            "motivo": self.motivo
        }
    
class DetallePedido:
    def __init__(self, id_detalle, id_ingrediente, cantidad_pedido):
        
        self.id_detalle = id_detalle
        self.id_ingrediente = id_ingrediente
        self.cantidad_pedido = cantidad_pedido
        self.validar_cantidad()

    def validar_cantidad(self):
        if self.id_detalle is None:
            raise ValueError("El detalle del pedido debe tener un id.")

        if self.id_ingrediente is None:
            raise ValueError("El detalle del pedido debe tener un ingrediente.")

        if self.cantidad_pedido <= 0:
            raise ValueError("La cantidad del pedido debe ser mayor a cero.")

    def convertir_a_diccionario(self):
        return {
            "id_detalle": self.id_detalle,
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
        if self.id_pedido is None:
            raise ValueError("El pedido debe tener un id.")

        if self.id_proveedor is None:
            raise ValueError("El pedido debe tener un proveedor.")

        if self.id_sucursal is None:
            raise ValueError("El pedido debe tener una sucursal.")

        if self.fecha == "":
            raise ValueError("El pedido debe tener fecha.")

        if self.estado == "":
            raise ValueError("El pedido debe tener estado.")

        if len(self.detalles) == 0:
            raise ValueError("Un pedido debe contener al menos un detalle.")

    def confirmar_pedido(self):
        self.validar_pedido()

        if self.estado == "confirmado":
            raise ValueError("El pedido ya fue confirmado.")

        self.estado = "confirmado"

    def convertir_a_diccionario(self):
        return {
            "id_pedido": self.id_pedido,
            "id_proveedor": self.id_proveedor,
            "id_sucursal": self.id_sucursal,
            "fecha": self.fecha,
            "estado": self.estado,
            "detalles": [detalle.convertir_a_diccionario() for detalle in self._detalles]
        }

class DetalleReceta:
    def __init__(self, id_detalle_receta, id_ingrediente, cantidad_ingrediente):
        self.id_detalle_receta = id_detalle_receta
        self.id_ingrediente = id_ingrediente
        self.cantidad_ingrediente = cantidad_ingrediente

        self.validar_cantidad()

    def validar_cantidad(self):
        if self.id_detalle_receta is None:
            raise ValueError("El detalle de receta debe tener un id.")

        if self.id_ingrediente is None:
            raise ValueError("El detalle de receta debe tener un ingrediente.")

        if self.cantidad_ingrediente <= 0:
            raise ValueError("La cantidad del ingrediente debe ser mayor a cero.")

    def convertir_a_diccionario(self):
        return {
            "id_detalle_receta": self.id_detalle_receta,
            "id_ingrediente": self.id_ingrediente,
            "cantidad_ingrediente": self.cantidad_ingrediente
        }
    
class Plato:
    def __init__(self, id_plato, nombre, descripcion, precio):
        if id_plato is None:
            raise ValueError("El plato debe tener un id.")

        if nombre == "":
            raise ValueError("El plato debe tener nombre.")

        if descripcion == "":
            raise ValueError("El plato debe tener descripción.")
        
        if precio <= 0:
            raise ValueError("El precio del plato debe ser mayor a cero.")

        self.id_plato = id_plato
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self._receta = []
        
    @property
    def receta(self):
        return tuple(self._receta)
    
    def agregar_ingrediente(self, detalle_receta):
        if not isinstance(detalle_receta, DetalleReceta):
            raise ValueError("Solo se pueden agregar objetos DetalleReceta.")

        self._receta.append(detalle_receta)

    def validar_receta(self):
        if len(self._receta) == 0:
            raise ValueError("El plato debe tener al menos un ingrediente en su receta.")

    def convertir_a_diccionario(self):
        return {
            "id_plato": self.id_plato,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "receta": [detalle.convertir_a_diccionario() for detalle in self.receta]
        }
