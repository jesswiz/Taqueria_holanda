from DOMAIN.entidades import Proveedor
from DATA.conexion import obtener_conexion

class ProveedorRepository:
    
    def obtener_todos(self):
        proveedores = []
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_proveedor, nombre, telefono, direccion, dui_nit FROM proveedores")
                resultados = cursor.fetchall()
                for fila in resultados:
                    proveedores.append(Proveedor(**fila))
        return proveedores

    def obtener_por_id(self, id_proveedor):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
                fila = cursor.fetchone()
                if fila:
                    return Proveedor(**fila)
        return None

    def obtener_por_dui_nit(self, dui_nit):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM proveedores WHERE dui_nit = %s", (dui_nit,))
                fila = cursor.fetchone()
                if fila:
                    return Proveedor(**fila)
        return None

    def agregar(self, proveedor):
        if not isinstance(proveedor, Proveedor):
            raise ValueError("Solo se pueden guardar objetos Proveedor.")
            
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                sql = """INSERT INTO proveedores (nombre, telefono, direccion, dui_nit)
                         VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (proveedor.nombre, proveedor.telefono, proveedor.direccion, proveedor.dui_nit))
                conexion.commit()
                proveedor.id_proveedor = cursor.lastrowid 
        return proveedor

    def actualizar(self, proveedor):
        if not isinstance(proveedor, Proveedor):
            raise ValueError("Solo se pueden actualizar objetos Proveedor.")
            
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                sql = """UPDATE proveedores 
                         SET nombre = %s, telefono = %s, direccion = %s, dui_nit = %s
                         WHERE id_proveedor = %s"""
                cursor.execute(
                    sql, 
                    (proveedor.nombre, proveedor.telefono, proveedor.direccion, proveedor.dui_nit, proveedor.id_proveedor)
                )
                conexion.commit()
        return proveedor

    def eliminar(self, id_proveedor):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                proveedor = self.obtener_por_id(id_proveedor)
                if proveedor:
                    cursor.execute("DELETE FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
                    conexion.commit()
                    return proveedor
        return None

proveedor_repository = ProveedorRepository()