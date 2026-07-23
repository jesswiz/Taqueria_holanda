from DOMAIN.entidades import DetallePedido, Pedido

class PedidoNoEncontradoError(Exception):
    pass

class DetalleNoEncontradoError(Exception):
    pass

class ConflictoPedidoError(Exception):
    pass

class ServicioPedido:
    def __init__(
        self,
        pedido_repository,
        proveedor_repository
    ):
        self.pedido_repository = pedido_repository
        self.proveedor_repository = proveedor_repository

    def listar_pedidos(self):
        pedidos = self.pedido_repository.obtener_todos()

        return [
            pedido.convertir_a_diccionario()
            for pedido in pedidos
        ]

    def obtener_pedido(self, id_pedido):
        pedido = self._buscar_pedido(id_pedido)

        return pedido.convertir_a_diccionario()

    def crear_pedido(
        self,
        id_pedido,
        id_proveedor,
        id_sucursal,
        fecha,
        estado,
        detalles
    ):
        pedido_existente = (
            self.pedido_repository.obtener_por_id(
                id_pedido
            )
        )

        if pedido_existente is not None:
            raise ConflictoPedidoError("Ya existe un pedido con ese id.")

        self._validar_proveedor_existente(
            id_proveedor
        )

        detalles_creados = self._crear_detalles(
            detalles
        )

        pedido = Pedido(
            id_pedido=id_pedido,
            id_proveedor=id_proveedor,
            id_sucursal=id_sucursal,
            fecha=fecha,
            estado=estado
        )

        for detalle in detalles_creados:
            pedido.agregar_detalle(detalle)

        pedido.validar_pedido()

        self.pedido_repository.agregar(pedido)

        return pedido.convertir_a_diccionario()

    def actualizar_pedido(
        self,
        id_pedido,
        id_proveedor,
        id_sucursal,
        fecha,
        estado,
        detalles
    ):
        self._buscar_pedido(id_pedido)

        self._validar_proveedor_existente(
            id_proveedor
        )

        detalles_creados = self._crear_detalles(
            detalles
        )

        pedido_actualizado = Pedido(
            id_pedido=id_pedido,
            id_proveedor=id_proveedor,
            id_sucursal=id_sucursal,
            fecha=fecha,
            estado=estado
        )

        for detalle in detalles_creados:
            pedido_actualizado.agregar_detalle(
                detalle
            )

        pedido_actualizado.validar_pedido()

        self.pedido_repository.actualizar(
            pedido_actualizado
        )

        return (
            pedido_actualizado.convertir_a_diccionario()
        )

    def eliminar_pedido(self, id_pedido):
        pedido = self.pedido_repository.eliminar(
            id_pedido
        )

        if pedido is None:
            raise PedidoNoEncontradoError("El pedido no existe.")

        return pedido.convertir_a_diccionario()

    def cambiar_estado(
        self,
        id_pedido,
        nuevo_estado
    ):
        pedido = self._buscar_pedido(id_pedido)

        pedido.cambiar_estado(nuevo_estado)

        self.pedido_repository.actualizar(pedido)

        return pedido.convertir_a_diccionario()

    def agregar_detalle(
        self,
        id_pedido,
        id_detalle,
        id_ingrediente,
        cantidad_pedido
    ):
        pedido = self._buscar_pedido(id_pedido)

        detalle_existente = pedido.obtener_detalle(
            id_detalle
        )

        if detalle_existente is not None:
            raise ConflictoPedidoError("Ya existe un detalle con ese id en el pedido.")

        detalle = DetallePedido(
            id_detalle=id_detalle,
            id_ingrediente=id_ingrediente,
            cantidad_pedido=cantidad_pedido
        )

        pedido.agregar_detalle(detalle)
        pedido.validar_pedido()

        self.pedido_repository.actualizar(pedido)

        return pedido.convertir_a_diccionario()

    def actualizar_detalle(
        self,
        id_pedido,
        id_detalle,
        id_ingrediente,
        cantidad_pedido
    ):
        pedido = self._buscar_pedido(id_pedido)

        detalle = pedido.obtener_detalle(
            id_detalle
        )

        if detalle is None:
            raise DetalleNoEncontradoError("El detalle del pedido no existe.")

        pedido.actualizar_detalle(
            id_detalle=id_detalle,
            id_ingrediente=id_ingrediente,
            cantidad_pedido=cantidad_pedido
        )

        pedido.validar_pedido()

        self.pedido_repository.actualizar(pedido)

        return pedido.convertir_a_diccionario()

    def eliminar_detalle(
        self,
        id_pedido,
        id_detalle
    ):
        pedido = self._buscar_pedido(id_pedido)

        detalle = pedido.obtener_detalle(
            id_detalle
        )

        if detalle is None:
            raise DetalleNoEncontradoError("El detalle del pedido no existe.")

        pedido.eliminar_detalle(id_detalle)

        self.pedido_repository.actualizar(pedido)

        return pedido.convertir_a_diccionario()

    def _buscar_pedido(self, id_pedido):
        pedido = (
            self.pedido_repository.obtener_por_id(
                id_pedido
            )
        )

        if pedido is None:
            raise PedidoNoEncontradoError("El pedido no existe.")

        return pedido

    def _validar_proveedor_existente(
        self,
        id_proveedor
    ):
        proveedor = (
            self.proveedor_repository.obtener_por_id(
                id_proveedor
            )
        )

        if proveedor is None:
            raise ValueError("No se puede registrar el pedido porque el proveedor no existe.")

    @staticmethod
    def _crear_detalles(detalles):
        if not isinstance(detalles, list):
            raise ValueError("Los detalles del pedido deben enviarse en una lista.")

        if len(detalles) == 0:
            raise ValueError("Un pedido debe contener al menos un detalle.")

        detalles_creados = []

        for datos_detalle in detalles:
            if not isinstance(datos_detalle, dict):
                raise ValueError("Cada detalle del pedido debe ser un objeto JSON.")

            try:
                detalle = DetallePedido(
                    id_detalle=(
                        datos_detalle["id_detalle"]
                    ),
                    id_ingrediente=(
                        datos_detalle["id_ingrediente"]
                    ),
                    cantidad_pedido=(
                        datos_detalle["cantidad_pedido"]
                    )
                )

            except KeyError as error:
                raise ValueError(f"Falta el campo obligatorio:{error.args[0]}.") from error

            detalles_creados.append(detalle)

        ids_detalles = [
            detalle.id_detalle
            for detalle in detalles_creados
        ]

        if len(ids_detalles) != len(set(ids_detalles)):
            raise ValueError("No se permiten ids de detalle repetidos en un pedido.")

        return detalles_creados