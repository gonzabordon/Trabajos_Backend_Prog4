from typing import Annotated, Sequence
from fastapi import Depends, HTTPException, status
from models.autor import Autor, AutorCreate
from repositories.autor_repository import AutorRepository


class AutorService:
    def __init__(self, repo: Annotated[AutorRepository, Depends()]):
        self.repo = repo

    def listar_autores(self) -> Sequence[Autor]:
        return self.repo.get_all()

    def create_autor(self, autor_data: AutorCreate) -> Autor:
        autor = Autor.model_validate(autor_data)
        return self.repo.save(autor)

    def get_autor(self, autor_id: int) -> Autor:
        autor = self.repo.get_by_id(autor_id)
        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Autor no encontrado",
            )
        return autor

    def update_autor(self, autor_id: int, autor_data: AutorCreate) -> Autor:
        autor = self.get_autor(autor_id)
        autor.nombre = autor_data.nombre
        autor.nacionalidad = autor_data.nacionalidad
        return self.repo.save(autor)

    def delete_autor(self, autor_id: int) -> None:
        autor = self.get_autor(autor_id)
        self.repo.delete(autor)