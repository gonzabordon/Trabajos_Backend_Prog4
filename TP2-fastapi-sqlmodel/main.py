from fastapi import FastAPI
from database import create_db_and_tables
from routers import autores, libros, socios, prestamos

app = FastAPI(title="Sistema de Biblioteca", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(autores.router, prefix="/autores", tags=["Autores"])
app.include_router(libros.router, prefix="/libros", tags=["Libros"])
app.include_router(socios.router, prefix="/socios", tags=["Socios"])
app.include_router(prestamos.router, prefix="/prestamos", tags=["Préstamos"])