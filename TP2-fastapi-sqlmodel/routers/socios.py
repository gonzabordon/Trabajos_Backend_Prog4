from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database import get_session
from models.socio import Socio, SocioCreate
from models.prestamo import Prestamo
from services import socio_service

router = APIRouter()

@router.get("/", response_model=list[Socio])
def listar_socios(session: Session = Depends(get_session)):
    return socio_service.listar_socios(session)

@router.post("/", response_model=Socio, status_code=status.HTTP_201_CREATED)
def create_socio(socio: SocioCreate, session: Session = Depends(get_session)):
    return socio_service.create_socio(session, socio)

@router.get("/{id}", response_model=Socio)
def get_socio(id: int, session: Session = Depends(get_session)):
    return socio_service.get_socio(session, id)

@router.put("/{id}", response_model=Socio)
def update_socio(id: int, socio_data: SocioCreate, session: Session = Depends(get_session)):
    return socio_service.update_socio(session, id, socio_data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_socio(id: int, session: Session = Depends(get_session)):
    socio_service.delete_socio(session, id)
    return None

@router.get("/{id}/prestamos", response_model=list[Prestamo])
def listar_prestamos_socio(id: int, activos: Optional[bool] = None, session: Session = Depends(get_session)):
    return socio_service.listar_prestamos_socio(session, id, activos)