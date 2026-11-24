from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status
from models.libro import Libro, LibroCreate
from services.libro_service import LibroService

router = APIRouter()


@router.get("/", response_model=list[Libro])
def listar_libros(
    service: Annotated[LibroService, Depends()],
    disponibles: Optional[bool] = None,
):
    return service.listar_libros(disponibles)


@router.post("/", response_model=Libro, status_code=status.HTTP_201_CREATED)
def create_libro(libro: LibroCreate, service: Annotated[LibroService, Depends()]):
    return service.create_libro(libro)


@router.get("/{id}", response_model=Libro)
def get_libro(id: int, service: Annotated[LibroService, Depends()]):
    return service.get_libro(id)


@router.put("/{id}", response_model=Libro)
def update_libro(
    id: int, libro_data: LibroCreate, service: Annotated[LibroService, Depends()]
):
    return service.update_libro(id, libro_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_libro(id: int, service: Annotated[LibroService, Depends()]):
    service.delete_libro(id)
    return None


@router.post("/{id}/autores/{autor_id}", status_code=status.HTTP_201_CREATED)
def asociar_autor(
    id: int, autor_id: int, service: Annotated[LibroService, Depends()]
):
    return service.asociar_autor_a_libro(id, autor_id)