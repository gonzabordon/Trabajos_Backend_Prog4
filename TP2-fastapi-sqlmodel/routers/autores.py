from typing import Annotated
from fastapi import APIRouter, Depends, status
from models.autor import Autor, AutorCreate
from services.autor_service import AutorService

router = APIRouter()


@router.get("/", response_model=list[Autor])
def listar_autores(service: Annotated[AutorService, Depends()]):
    return service.listar_autores()


@router.post("/", response_model=Autor, status_code=status.HTTP_201_CREATED)
def create_autor(autor: AutorCreate, service: Annotated[AutorService, Depends()]):
    return service.create_autor(autor)


@router.get("/{id}", response_model=Autor)
def get_autor(id: int, service: Annotated[AutorService, Depends()]):
    return service.get_autor(id)


@router.put("/{id}", response_model=Autor)
def update_autor(
    id: int, autor_data: AutorCreate, service: Annotated[AutorService, Depends()]
):
    return service.update_autor(id, autor_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_autor(id: int, service: Annotated[AutorService, Depends()]):
    service.delete_autor(id)
    return None