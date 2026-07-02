from flask import Flask, jsonify, request
#from ROUTES.inventario_routes import inventario_bp
# Estas líneas quedan comentadas temporalmente porque el archivo
# ROUTES/inventario_routes.py todavía no ha sido creado.
# Cuando la parte de ROUTES esté lista, se deben descomentar.

app = Flask(__name__)

#app.register_blueprint(inventario_bp)
# Aquí se registrarían las rutas externas del inventario.
# Por ahora queda comentado porque depende del archivo inventario_routes.py

@app.route("/")
def inicio():
    return {
        "mensaje": "API de Taquería Holanda funcionando correctamente",
        "capas": {
            "ROUTES": "Capa de presentación",
            "DOMAIN": "Capa de lógica y reglas del negocio",
            "DATA": "Capa de datos"
        }
    }


if __name__ == "__main__":
    app.run(debug=True)


