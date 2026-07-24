from DOMAIN.entidades import Plato, DetalleReceta
from DATA.conexion import obtener_conexion

class PlatoRepository:
    
    def obtener_todos(self):
        platos = []
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_plato, nombre, descripcion, precio FROM platos")
                resultados = cursor.fetchall()
                for fila in resultados:
                    platos.append(Plato(**fila))
        return platos

    def obtener_por_id(self, id_plato):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                # Primero buscamos el plato base
                cursor.execute("SELECT id_plato, nombre, descripcion, precio FROM platos WHERE id_plato = %s", (id_plato,))
                fila_plato = cursor.fetchone()
                
                if fila_plato:
                    plato = Plato(**fila_plato)
                    
                    # Luego buscamos los ingredientes que componen la receta de este plato
                    cursor.execute("SELECT id_detalle_receta, id_ingrediente, cantidad_ingrediente FROM detalles_receta WHERE id_plato = %s", (id_plato,))
                    detalles = cursor.fetchall()
                    
                    for detalle_fila in detalles:
                        # Creamos el objeto DetalleReceta y lo agregamos al plato
                        detalle = DetalleReceta(**detalle_fila)
                        plato.agregar_ingrediente(detalle)
                        
                    return plato
        return None

    def agregar(self, plato):
        if not isinstance(plato, Plato):
            raise ValueError("Solo se pueden guardar objetos Plato")

        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                # 1. Insertamos el plato principal
                sql_plato = "INSERT INTO platos (nombre, descripcion, precio) VALUES (%s, %s, %s)"
                cursor.execute(sql_plato, (plato.nombre, plato.descripcion, plato.precio))
                plato.id_plato = cursor.lastrowid
                
                # 2. Insertamos cada detalle de la receta asociado a este nuevo plato
                sql_detalle = "INSERT INTO detalles_receta (id_plato, id_ingrediente, cantidad_ingrediente) VALUES (%s, %s, %s)"
                for detalle in plato.receta:
                    cursor.execute(sql_detalle, (plato.id_plato, detalle.id_ingrediente, detalle.cantidad_ingrediente))
                
                conexion.commit()
                
        return plato

plato_repository = PlatoRepository()