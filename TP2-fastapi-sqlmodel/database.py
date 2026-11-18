from sqlmodel import create_engine, Session, SQLModel
from models.autor import Autor
from models.libro import Libro
from models.libro_autor import LibroAutor
from models.socio import Socio
from models.prestamo import Prestamo

sqlite_file_name = "biblioteca.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
