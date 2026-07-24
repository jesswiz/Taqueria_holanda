from DOMAIN.entidades import Ingrediente
from DATA.conexion import obtener_conexion

class IngredienteRepository:
    
    def obtener_todos(self):
        ingredientes = []
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_ingrediente, nombre, unidad_medida FROM ingredientes")
                resultados = cursor.fetchall()
                for fila in resultados:
                    ingredientes.append(Ingrediente(**fila))
        return ingredientes

    def obtener_por_id(self, id_ingrediente):
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT id_ingrediente, nombre, unidad_medida FROM ingredientes WHERE id_ingrediente = %s", 
                    (id_ingrediente,)
                )
                fila = cursor.fetchone()
                if fila:
                    return Ingrediente(**fila)
        return None

ingrediente_repository = IngredienteRepository()