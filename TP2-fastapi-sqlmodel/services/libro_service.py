from typing import Annotated, Optional, Sequence
from fastapi import Depends, HTTPException, status
from models.libro import Libro, LibroCreate
from models.libro_autor import LibroAutor
from repositories.autor_repository import AutorRepository
from repositories.libro_repository import LibroRepository


class LibroService:
    def __init__(
        self,
        libro_repo: Annotated[LibroRepository, Depends()],
        autor_repo: Annotated[AutorRepository, Depends()],
    ):
        self.libro_repo = libro_repo
        self.autor_repo = autor_repo

    def listar_libros(self, disponibles: Optional[bool] = None) -> Sequence[Libro]:
        return self.libro_repo.get_all(disponibles=disponibles)

    def create_libro(self, libro_data: LibroCreate) -> Libro:
        if self.libro_repo.get_by_isbn(libro_data.isbn):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El ISBN ya está registrado",
            )
        libro = Libro.model_validate(libro_data)
        return self.libro_repo.save(libro)

    def get_libro(self, libro_id: int) -> Libro:
        libro = self.libro_repo.get_by_id(libro_id)
        if not libro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Libro no encontrado",
            )
        return libro

    def update_libro(self, libro_id: int, libro_data: LibroCreate) -> Libro:
        libro = self.get_libro(libro_id)
        libro_existente = self.libro_repo.get_by_isbn(libro_data.isbn)
        if libro_existente and libro_existente.id != libro_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El ISBN ya está registrado",
            )
        libro.titulo = libro_data.titulo
        libro.isbn = libro_data.isbn
        libro.stock = libro_data.stock
        libro.anio = libro_data.anio
        return self.libro_repo.save(libro)

    def delete_libro(self, libro_id: int) -> None:
        libro = self.get_libro(libro_id)
        self.libro_repo.delete(libro)

    def asociar_autor_a_libro(self, libro_id: int, autor_id: int) -> dict[str, str]:
        libro = self.libro_repo.get_by_id(libro_id)
        autor = self.autor_repo.get_by_id(autor_id)
        if not libro or not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Libro o Autor no encontrado",
            )

        if self.libro_repo.get_autor_link(libro_id, autor_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El autor ya está asociado a este libro",
            )

        asociacion = LibroAutor(libro_id=libro_id, autor_id=autor_id)
        self.libro_repo.add_autor_link(asociacion)
        return {"message": "Autor asociado correctamente al libro"}