from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.socio import Socio, SocioCreate
from models.prestamo import Prestamo

def listar_socios(session: Session) -> list[Socio]:
    return session.exec(select(Socio)).all()

def create_socio(session: Session, socio_data: SocioCreate) -> Socio:
    socio = Socio.model_validate(socio_data)
    try:
        session.add(socio)
        session.commit()
        session.refresh(socio)
        return socio
    except IntegrityError:
        session.rollback()
        # Regla 8: Email duplicado (409)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")

def get_socio(session: Session, socio_id: int) -> Socio:
    socio = session.get(Socio, socio_id)
    if not socio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
    return socio

def update_socio(session: Session, socio_id: int, socio_data: SocioCreate) -> Socio:
    socio = get_socio(session, socio_id)
    socio.nombre = socio_data.nombre
    socio.email = socio_data.email
    socio.activo = socio_data.activo
    try:
        session.add(socio)
        session.commit()
        session.refresh(socio)
        return socio
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")

def delete_socio(session: Session, socio_id: int) -> None:
    socio = get_socio(session, socio_id)
    session.delete(socio)
    session.commit()

def listar_prestamos_socio(session: Session, socio_id: int, activos: Optional[bool] = None) -> list[Prestamo]:
    get_socio(session, socio_id)
    query = select(Prestamo).where(Prestamo.socio_id == socio_id)
    if activos is True:
        query = query.where(Prestamo.fecha_devolucion == None)
    elif activos is False:
        query = query.where(Prestamo.fecha_devolucion != None)
    return session.exec(query).all()