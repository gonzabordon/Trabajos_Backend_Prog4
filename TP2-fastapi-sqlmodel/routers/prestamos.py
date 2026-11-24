from typing import Annotated
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from models.prestamo import Prestamo
from services.prestamo_service import PrestamoService

router = APIRouter()


class PrestamoCreate(BaseModel):
    socio_id: int
    libro_id: int


@router.get("/", response_model=list[Prestamo])
def listar_prestamos(service: Annotated[PrestamoService, Depends()]):
    return service.listar_prestamos()


@router.post("/", response_model=Prestamo, status_code=status.HTTP_201_CREATED)
def create_prestamo(
    data: PrestamoCreate, service: Annotated[PrestamoService, Depends()]
):
    return service.registrar_prestamo(data.socio_id, data.libro_id)


@router.post("/{id}/devolucion", response_model=Prestamo)
def return_prestamo(id: int, service: Annotated[PrestamoService, Depends()]):
    return service.registrar_devolucion(id)