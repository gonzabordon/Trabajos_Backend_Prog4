from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status
from models.prestamo import Prestamo
from models.socio import Socio, SocioCreate
from services.socio_service import SocioService

router = APIRouter()


@router.get("/", response_model=list[Socio])
def listar_socios(service: Annotated[SocioService, Depends()]):
    return service.listar_socios()


@router.post("/", response_model=Socio, status_code=status.HTTP_201_CREATED)
def create_socio(socio: SocioCreate, service: Annotated[SocioService, Depends()]):
    return service.create_socio(socio)


@router.get("/{id}", response_model=Socio)
def get_socio(id: int, service: Annotated[SocioService, Depends()]):
    return service.get_socio(id)


@router.put("/{id}", response_model=Socio)
def update_socio(
    id: int, socio_data: SocioCreate, service: Annotated[SocioService, Depends()]
):
    return service.update_socio(id, socio_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_socio(id: int, service: Annotated[SocioService, Depends()]):
    service.delete_socio(id)
    return None


@router.get("/{id}/prestamos", response_model=list[Prestamo])
def listar_prestamos_socio(
    id: int,
    service: Annotated[SocioService, Depends()],
    activos: Optional[bool] = None,
):
    return service.listar_prestamos_socio(id, activos)