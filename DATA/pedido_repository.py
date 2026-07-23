from DOMAIN.entidades import Pedido
class PedidoRepository:
    def __init__(self):
        self.pedidos = {}

    def obtener_todos(self):
        return list(self.pedidos.values())

    def obtener_por_id(self, id_pedido):
        return self.pedidos.get(id_pedido)

    def agregar(self, pedido):
        if not isinstance(pedido, Pedido):
            raise ValueError("Solo se pueden guardar objetos Pedido.")

        self.pedidos[pedido.id_pedido] = pedido
        return pedido

    def actualizar(self, pedido):
        if not isinstance(pedido, Pedido):
            raise ValueError("Solo se pueden actualizar objetos Pedido.")

        self.pedidos[pedido.id_pedido] = pedido
        return pedido

    def eliminar(self, id_pedido):
        return self.pedidos.pop(id_pedido, None)

pedido_repository = PedidoRepository()