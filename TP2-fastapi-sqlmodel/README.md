# API REST - Sistema de Gestión de Biblioteca

API RESTful desarrollada con **FastAPI** y **SQLModel** para administrar el catálogo de libros, autores, socios y el circuito completo de préstamos y devoluciones de una biblioteca, aplicando arquitectura modular en capas, validaciones de negocio y pruebas automatizadas con **100 % de cobertura**.

---

## Tecnologías Utilizadas

* **Python 3.13+**
* **FastAPI** — Framework web para la construcción de endpoints REST y documentación automática OpenAPI/Swagger.
* **SQLModel** — ORM y validación de esquemas basado en SQLAlchemy y Pydantic.
* **SQLite** — Base de datos relacional embebida.
* **Uvicorn** — Servidor ASGI de alto rendimiento.
* **Pytest / Pytest-cov / HTTPX** — Suite de pruebas unitarias, de integración y medición de cobertura de código.

---

## Arquitectura y Estructura del Proyecto

El proyecto sigue una separación de responsabilidades en capas (`models`, `services`, `routers` y `tests`):

```text
TP2-fastpi-sqlmodel/
├── main.py                     # Punto de entrada de la aplicación y registro de routers
├── database.py                 # Configuración del motor SQLite, creación de tablas y sesiones
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                  # Exclusión de entorno virtual, cachés y base local
├── models/                     # Modelos de tablas (SQLModel) y esquemas de entrada (*Create)
│   ├── __init__.py
│   ├── autor.py
│   ├── libro.py
│   ├── libro_autor.py
│   ├── socio.py
│   └── prestamo.py
├── services/                   # Lógica de negocio, reglas de validación y transacciones
│   ├── __init__.py
│   ├── autor_service.py
│   ├── libro_service.py
│   ├── socio_service.py
│   └── prestamo_service.py
├── routers/                    # Definición de rutas HTTP, parámetros y códigos de estado
│   ├── __init__.py
│   ├── autores.py
│   ├── libros.py
│   ├── socios.py
│   └── prestamos.py
└── tests/                      # Tests automatizados de integración y reglas de negocio
    ├── __init__.py
    ├── conftest.py
    ├── test_database.py
    ├── test_autores.py
    ├── test_libros.py
    ├── test_socios.py
    └── test_prestamos.py
```

### Modelo de Datos y Relaciones

* **`Libro` N–N `Autor`:** Relación muchos a muchos resuelta mediante la tabla intermedia `LibroAutor` (clave primaria compuesta por `libro_id` y `autor_id`).
* **`Préstamo` N–1 `Socio`:** Cada préstamo pertenece a un único socio mediante la clave foránea `socio_id`.
* **`Préstamo` N–1 `Libro`:** Cada préstamo referencia a un único libro mediante la clave foránea `libro_id`.

---

## Reglas de Negocio Implementadas

1. **Límite de préstamos activos:** Un socio no puede tener más de **3 préstamos activos** simultáneamente (`409 Conflict`).
2. **Control de stock:** No se permite prestar un libro con `stock <= 0` (`409 Conflict`). Al confirmar un préstamo, se descuenta `1` unidad del stock del libro.
3. **Estado del socio:** Un socio inactivo (`activo = false`) no puede solicitar préstamos (`403 Forbidden`).
4. **Plazo de préstamo:** Todo préstamo se registra con un vencimiento automático de **14 días** corridos a partir de la fecha de emisión.
5. **Devolución y cálculo de multas:** Al registrar una devolución, se repone `1` unidad al stock del libro. Si la fecha de devolución supera `fecha_vencimiento`, se aplica una multa de **$100 por día de atraso**; en caso contrario, la multa es `$0`.
6. **Prevención de doble devolución:** No se permite volver a devolver un préstamo que ya tiene `fecha_devolucion` registrada (`409 Conflict`).
7. **Validación de existencia:** Cualquier operación sobre un `autor`, `libro`, `socio` o `prestamo` inexistente devuelve `404 Not Found`.
8. **Unicidad de registros:** El `isbn` de cada libro y el `email` de cada socio son únicos; intentar registrar o actualizar con un valor duplicado devuelve `409 Conflict`. Tampoco se permite asociar dos veces el mismo autor a un mismo libro (`409 Conflict`).

---

## Endpoints de la API

### Autores (`/autores`)

| Método | Ruta | Descripción | Códigos HTTP |
| :--- | :--- | :--- | :--- |
| `GET` | `/autores/` | Lista todos los autores registrados. | `200` |
| `POST` | `/autores/` | Crea un nuevo autor. | `201` |
| `GET` | `/autores/{id}` | Obtiene un autor por su ID. | `200`, `404` |
| `PUT` | `/autores/{id}` | Actualiza los datos de un autor existente. | `200`, `404` |
| `DELETE` | `/autores/{id}` | Elimina un autor. | `204`, `404` |

### Libros (`/libros`)

| Método | Ruta | Descripción | Códigos HTTP |
| :--- | :--- | :--- | :--- |
| `GET` | `/libros/` | Lista libros. Soporta `?disponibles=true` (`stock > 0`) y `?disponibles=false` (`stock == 0`). | `200` |
| `POST` | `/libros/` | Crea un nuevo libro validando unicidad de ISBN. | `201`, `409` |
| `GET` | `/libros/{id}` | Obtiene un libro por su ID. | `200`, `404` |
| `PUT` | `/libros/{id}` | Actualiza los datos de un libro. | `200`, `404`, `409` |
| `DELETE` | `/libros/{id}` | Elimina un libro. | `204`, `404` |
| `POST` | `/libros/{id}/autores/{autor_id}` | Asocia un autor existente a un libro (relación N–N). | `201`, `404`, `409` |

### Socios (`/socios`)

| Método | Ruta | Descripción | Códigos HTTP |
| :--- | :--- | :--- | :--- |
| `GET` | `/socios/` | Lista todos los socios. | `200` |
| `POST` | `/socios/` | Registra un nuevo socio validando unicidad de email. | `201`, `409` |
| `GET` | `/socios/{id}` | Obtiene un socio por su ID. | `200`, `404` |
| `PUT` | `/socios/{id}` | Actualiza los datos de un socio. | `200`, `404`, `409` |
| `DELETE` | `/socios/{id}` | Elimina un socio. | `204`, `404` |
| `GET` | `/socios/{id}/prestamos` | Lista los préstamos de un socio. Soporta `?activos=true` y `?activos=false`. | `200`, `404` |

### Préstamos (`/prestamos`)

| Método | Ruta | Descripción | Códigos HTTP |
| :--- | :--- | :--- | :--- |
| `GET` | `/prestamos/` | Lista el historial completo de préstamos. | `200` |
| `POST` | `/prestamos/` | Registra un nuevo préstamo aplicando las reglas de negocio y descontando stock. | `201`, `403`, `404`, `409` |
| `POST` | `/prestamos/{id}/devolucion` | Registra la devolución de un préstamo, repone stock y calcula multas por atraso. | `200`, `404`, `409` |

---

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
```

### 2. Crear y activar el entorno virtual

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

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Levantar el servidor de desarrollo

```bash
uvicorn main:app --reload
```
*(También puedes ejecutar `fastapi dev main.py` si utilizas FastAPI CLI).*

Una vez iniciado el servidor, accede a la documentación interactiva en tu navegador:
* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Ejecución de Tests y Cobertura

Las pruebas utilizan una base de datos **SQLite en memoria** (`StaticPool`) aislada por test, sin modificar el archivo `biblioteca.db` de desarrollo.

Para ejecutar toda la suite de pruebas desde la raíz del proyecto:

```bash
pytest -v
```

Para ejecutar las pruebas junto con el reporte de cobertura de código:

```bash
pytest --cov=models --cov=routers --cov=services --cov=main --cov=database --cov-report=term-missing
```
