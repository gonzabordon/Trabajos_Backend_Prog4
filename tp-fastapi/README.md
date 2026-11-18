# API REST - Gestión de Usuarios y Películas (FastAPI)

API RESTful desarrollada con **FastAPI** y **Pydantic** para administrar usuarios y un catálogo de películas en memoria. Permite realizar operaciones CRUD completas, validación automática de esquemas de datos y filtrado dinámico mediante parámetros de consulta (*query parameters*).

---

## Tecnologías Utilizadas

* **Python 3.10+**
* **FastAPI** — Framework web moderno y de alto rendimiento para construir APIs REST.
* **Pydantic** — Validación de datos, tipado estático y definición de esquemas de entrada/salida.
* **Uvicorn** — Servidor ASGI para ejecutar la aplicación.

---

## Estructura del Proyecto

```text
.
├── main.py                 # Punto de entrada de la API, datos iniciales y definición de endpoints
├── requirements.txt        # Dependencias necesarias para ejecutar el proyecto
├── .gitignore              # Archivos y carpetas excluidos del control de versiones
└── models/                 # Esquemas Pydantic para validación de requests y responses
    ├── __init__.py
    ├── users.py            # Modelos de Usuario (User, UserUpdate y respuestas)
    └── peliculas.py        # Modelos de Película (Pelicula, PeliculaUpdate y respuestas)
```

---

## Instalación y Ejecución

Sigue estos pasos desde una terminal ubicada en la carpeta raíz del proyecto:

### 1. Crear y activar el entorno virtual

**En Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar las dependencias

Con el entorno virtual activado, instala los paquetes listados en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Levantar la aplicación

Ejecuta el servidor de desarrollo con Uvicorn (con recarga automática ante cambios en el código):

```bash
uvicorn main:app --reload
```

*(Alternativamente, si tienes instalado FastAPI CLI, puedes iniciar el servidor con `fastapi dev main.py`).*

Una vez iniciado, verás en la consola que el servidor está corriendo en **`http://127.0.0.1:8000`**.

---

## Documentación Interactiva (Swagger UI)

FastAPI genera automáticamente una interfaz gráfica interactiva para explorar y probar todos los endpoints sin necesidad de herramientas externas:

1. Con el servidor en ejecución, abre tu navegador web e ingresa a:
   * **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * *(También disponible en formato alternativo ReDoc en [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc))*
2. Selecciona cualquiera de los endpoints listados (`GET`, `POST`, `PUT`, `DELETE`) para desplegar su detalle.
3. Haz clic en el botón **"Try it out"** ubicado a la derecha del endpoint.
4. Completa los parámetros requeridos o edita el cuerpo JSON (*Request body*) según corresponda.
5. Presiona **"Execute"** para enviar la petición y visualizar el código de estado HTTP y la respuesta JSON del servidor.

> **Nota sobre datos iniciales:** Al iniciar la aplicación, la API ya cuenta con 2 usuarios (`id: 1` y `id: 2`) y 2 películas (`id: 1` y `id: 2`) precargados en memoria para facilitar las pruebas inmediatas en `/docs`.

---

## Endpoints Disponibles

### General

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Endpoint raíz de bienvenida que verifica el funcionamiento de la API. |

### Usuarios (`/user`)

| Método | Ruta | Descripción | Parámetros / Cuerpo |
| :--- | :--- | :--- | :--- |
| `GET` | `/user` | Lista todos los usuarios registrados. | Query opcional: `?is_active=true` o `?is_active=false` |
| `POST` | `/user` | Crea y agrega un nuevo usuario. | JSON: `id`, `name`, `is_active` (opcional, por defecto `true`) |
| `PUT` | `/user/{id}` | Modifica los datos de un usuario existente. | Path: `id` \| JSON opcional: `name`, `is_active` |
| `DELETE` | `/user/{id}` | Elimina un usuario por su ID. | Path: `id` |

### Películas (`/pelicula`)

| Método | Ruta | Descripción | Parámetros / Cuerpo |
| :--- | :--- | :--- | :--- |
| `GET` | `/pelicula` | Lista todas las películas del catálogo. | Query opcional: `?en_stock=true` o `?en_stock=false` |
| `GET` | `/pelicula/{pelicula_id}` | Obtiene el detalle de una película específica. | Path: `pelicula_id` |
| `POST` | `/pelicula` | Agrega una nueva película al catálogo. | JSON: `id`, `titulo`, `director`, `genero`, `anio`, `en_stock` (opcional, por defecto `true`) |
| `PUT` | `/pelicula/{id}` | Actualiza parcialmente los datos de una película. | Path: `id` \| JSON opcional: `titulo`, `director`, `genero`, `anio`, `en_stock` |
| `DELETE` | `/pelicula/{id}` | Elimina una película por su ID. | Path: `id` |