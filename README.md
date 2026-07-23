API Taquería Holanda
API desarrollada con Python y Flask para gestionar proveedores, pedidos, inventario, recetas y otros procesos internos de Taquería Holanda.

Arquitectura
El proyecto utiliza una arquitectura en capas:

-ROUTES: recibe solicitudes HTTP y devuelve respuestas JSON.
-DOMAIN: contiene las entidades, validaciones y lógica del negocio.
-DATA: contiene los repositorios y el acceso a los datos.


Estructura
TAQUERIA_HOLANDA/
├── DATA/
├── DOMAIN/
├── ROUTES/
├── app.py
├── requirements.txt
└── README.md


Instalación
Clonar el repositorio:
bash
git clone URL_DEL_REPOSITORIO
cd Taqueria_holanda

Crear y activar el entorno virtual:
bash
python -m venv .venv
.venv\Scripts\activate

Instalar las dependencias:
bash
pip install -r requirements.txt

Configuración
Crear un archivo .env en la raíz del proyecto:

.env
DB_HOST=localhost
DB_PORT=3306
DB_USER=usuario
DB_PASSWORD=contraseña
DB_NAME=taqueria_holanda

El archivo .env no debe subirse a GitHub.

Ejecución
bash
python app.py

La API estará disponible en:
http://127.0.0.1:5000

Endpoints principales
