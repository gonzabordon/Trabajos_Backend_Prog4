from typing import Annotated, Optional, Sequence
from fastapi import Depends
from sqlmodel import Session, select
from database import get_session
from models.libro import Libro
from models.libro_autor import LibroAutor


class LibroRepository:
    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def get_all(self, disponibles: Optional[bool] = None) -> Sequence[Libro]:
        query = select(Libro)
        if disponibles is True:
            query = query.where(Libro.stock > 0)
        elif disponibles is False:
            query = query.where(Libro.stock == 0)
        return self.session.exec(query).all()

    def get_by_id(self, libro_id: int) -> Optional[Libro]:
        return self.session.get(Libro, libro_id)

    def get_by_isbn(self, isbn: str) -> Optional[Libro]:
        statement = select(Libro).where(Libro.isbn == isbn)
        return self.session.exec(statement).first()

    def save(self, libro: Libro) -> Libro:
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def delete(self, libro: Libro) -> None:
        self.session.delete(libro)
        self.session.commit()

    def get_autor_link(self, libro_id: int, autor_id: int) -> Optional[LibroAutor]:
        return self.session.get(LibroAutor, (libro_id, autor_id))

    def add_autor_link(self, link: LibroAutor) -> LibroAutor:
        self.session.add(link)
        self.session.commit()
        self.session.refresh(link)
        return link