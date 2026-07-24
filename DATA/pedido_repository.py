from DOMAIN.entidades import Pedido, DetallePedido
from DATA.conexion import obtener_conexion

class PedidoRepository:
    
    def obtener_todos(self):
        pedidos = []
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_pedido, id_proveedor, id_sucursal, fecha, estado FROM pedidos")
                resultados = cursor.fetchall()
                for fila in resultados:
                    pedido = Pedido(**fila)
                    
                    # Traemos también los detalles de cada pedido
                    cursor.execute(
                        "SELECT id_detalle, id_ingrediente, cantidad_pedido FROM detalles_pedido WHERE id_pedido = %s", 
                        (pedido.id_pedido,)
                    )
                    detalles = cursor.fetchall()
                    for det_fila in detalles:
                        pedido.agregar_detalle(DetallePedido(**det_fila))
                        
                    pedidos.append(pedido)
        return pedidos

    def obtener_por_id(self, id_pedido):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT id_pedido, id_proveedor, id_sucursal, fecha, estado FROM pedidos WHERE id_pedido = %s", 
                    (id_pedido,)
                )
                fila = cursor.fetchone()
                
                if fila:
                    pedido = Pedido(**fila)
                    cursor.execute(
                        "SELECT id_detalle, id_ingrediente, cantidad_pedido FROM detalles_pedido WHERE id_pedido = %s", 
                        (id_pedido,)
                    )
                    detalles = cursor.fetchall()
                    for det_fila in detalles:
                        pedido.agregar_detalle(DetallePedido(**det_fila))
                        
                    return pedido
        return None

    def agregar(self, pedido):
        if not isinstance(pedido, Pedido):
            raise ValueError("Solo se pueden guardar objetos Pedido.")
            
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                sql_pedido = """INSERT INTO pedidos (id_proveedor, id_sucursal, fecha, estado) 
                                VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql_pedido, (pedido.id_proveedor, pedido.id_sucursal, pedido.fecha, pedido.estado))
                pedido.id_pedido = cursor.lastrowid
                
                sql_detalle = """INSERT INTO detalles_pedido (id_pedido, id_ingrediente, cantidad_pedido) 
                                 VALUES (%s, %s, %s)"""
                for detalle in pedido.detalles:
                    cursor.execute(sql_detalle, (pedido.id_pedido, detalle.id_ingrediente, detalle.cantidad_pedido))
                    
                conexion.commit()
        return pedido

    def actualizar(self, pedido):
        if not isinstance(pedido, Pedido):
            raise ValueError("Solo se pueden actualizar objetos Pedido.")
            
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                # Actualizamos los datos principales del pedido
                sql_pedido = """UPDATE pedidos 
                                SET id_proveedor = %s, id_sucursal = %s, fecha = %s, estado = %s 
                                WHERE id_pedido = %s"""
                cursor.execute(sql_pedido, (pedido.id_proveedor, pedido.id_sucursal, pedido.fecha, pedido.estado, pedido.id_pedido))
                
                # La forma más limpia de actualizar detalles es borrarlos y volver a insertarlos
                cursor.execute("DELETE FROM detalles_pedido WHERE id_pedido = %s", (pedido.id_pedido,))
                
                sql_detalle = """INSERT INTO detalles_pedido (id_pedido, id_ingrediente, cantidad_pedido) 
                                 VALUES (%s, %s, %s)"""
                for detalle in pedido.detalles:
                    cursor.execute(sql_detalle, (pedido.id_pedido, detalle.id_ingrediente, detalle.cantidad_pedido))
                    
                conexion.commit()
        return pedido

    def eliminar(self, id_pedido):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                pedido = self.obtener_por_id(id_pedido)
                if pedido:
                    # Borramos primero los hijos (detalles) y luego el padre (pedido) para evitar errores de llave foránea
                    cursor.execute("DELETE FROM detalles_pedido WHERE id_pedido = %s", (id_pedido,))
                    cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id_pedido,))
                    conexion.commit()
                    return pedido
        return None

pedido_repository = PedidoRepository()