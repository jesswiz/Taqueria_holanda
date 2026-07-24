from DOMAIN.entidades import Inventario
from DATA.conexion import obtener_conexion

class InventarioRepository:
    
    def obtener_todos(self):
        inventarios = []
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_inventario, id_sucursal, id_ingrediente, cantidad_disponible FROM inventario")
                resultados = cursor.fetchall()
                for fila in resultados:
                    inventarios.append(Inventario(**fila))
        return inventarios

    def obtener_por_id(self, id_inventario):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM inventario WHERE id_inventario = %s", (id_inventario,))
                fila = cursor.fetchone()
                if fila:
                    return Inventario(**fila)
        return None

    def obtener_por_sucursal(self, id_sucursal):
        inventarios = []
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM inventario WHERE id_sucursal = %s", (id_sucursal,))
                resultados = cursor.fetchall()
                for fila in resultados:
                    inventarios.append(Inventario(**fila))
        return inventarios
        
    def obtener_por_sucursal_e_ingrediente(self, id_sucursal, id_ingrediente):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM inventario WHERE id_sucursal = %s AND id_ingrediente = %s", 
                    (id_sucursal, id_ingrediente)
                )
                fila = cursor.fetchone()
                if fila:
                    return Inventario(**fila)
        return None

    def actualizar(self, inventario):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                # Actualizamos la cantidad en stock de la tabla principal
                sql = "UPDATE inventario SET cantidad_disponible = %s WHERE id_inventario = %s"
                cursor.execute(sql, (inventario.cantidad_disponible, inventario.id_inventario))
                
                # Si tienes una tabla de movimientos (movimientos_inventario), se inserta el historial aquí.
                # Verificamos si la entidad generó movimientos en memoria durante este proceso.
                if inventario.movimientos:
                    ultimo_movimiento = inventario.movimientos[-1] # Tomamos la transacción más reciente
                    sql_mov = """INSERT INTO movimientos_inventario 
                                 (id_inventario, tipo_accion, cantidad_movida, fecha_accion, motivo) 
                                 VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(sql_mov, (
                        inventario.id_inventario, 
                        ultimo_movimiento.tipo_accion, 
                        ultimo_movimiento.cantidad_movida, 
                        ultimo_movimiento.fecha_accion, 
                        ultimo_movimiento.motivo
                    ))
                    
                conexion.commit()
        return inventario

inventario_repository = InventarioRepository()