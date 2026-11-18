from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from pydantic import BaseModel
from database import get_session
from models.prestamo import Prestamo
from services import prestamo_service

router = APIRouter()

class PrestamoCreate(BaseModel):
    socio_id: int
    libro_id: int

@router.get("/", response_model=list[Prestamo])
def listar_prestamos(session: Session = Depends(get_session)):
    return prestamo_service.listar_prestamos(session)

@router.post("/", response_model=Prestamo, status_code=status.HTTP_201_CREATED)
def create_prestamo(data: PrestamoCreate, session: Session = Depends(get_session)):
    return prestamo_service.registrar_prestamo(session, data.socio_id, data.libro_id)

@router.post("/{id}/devolucion", response_model=Prestamo)
def return_prestamo(id: int, session: Session = Depends(get_session)):
    return prestamo_service.registrar_devolucion(session, id)