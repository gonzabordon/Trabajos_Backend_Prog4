from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.libro import Libro, LibroCreate
from models.autor import Autor
from models.libro_autor import LibroAutor

def listar_libros(session: Session, disponibles: Optional[bool] = None) -> list[Libro]:
    query = select(Libro)
    if disponibles is True:
        query = query.where(Libro.stock > 0)
    elif disponibles is False:
        query = query.where(Libro.stock == 0)
    return session.exec(query).all()

def create_libro(session: Session, libro_data: LibroCreate) -> Libro:
    libro = Libro.model_validate(libro_data)
    try:
        session.add(libro)
        session.commit()
        session.refresh(libro)
        return libro
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El ISBN ya está registrado")

def get_libro(session: Session, libro_id: int) -> Libro:
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    return libro

def update_libro(session: Session, libro_id: int, libro_data: LibroCreate) -> Libro:
    libro = get_libro(session, libro_id)
    libro.titulo = libro_data.titulo
    libro.isbn = libro_data.isbn
    libro.stock = libro_data.stock
    libro.anio = libro_data.anio
    try:
        session.add(libro)
        session.commit()
        session.refresh(libro)
        return libro
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El ISBN ya está registrado")

def delete_libro(session: Session, libro_id: int) -> None:
    libro = get_libro(session, libro_id)
    session.delete(libro)
    session.commit()

def asociar_autor_a_libro(session: Session, libro_id: int, autor_id: int) -> dict[str, str]:
    libro = session.get(Libro, libro_id)
    autor = session.get(Autor, autor_id)
    if not libro or not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro o Autor no encontrado")

    relacion_existente = session.get(LibroAutor, (libro_id, autor_id))
    if relacion_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El autor ya está asociado a este libro")

    asociacion = LibroAutor(libro_id=libro_id, autor_id=autor_id)
    session.add(asociacion)
    session.commit()
    return {"message": "Autor asociado correctamente al libro"}