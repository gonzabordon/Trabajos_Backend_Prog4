from typing import Annotated, Optional, Sequence
from fastapi import Depends
from sqlmodel import Session, select
from database import get_session
from models.prestamo import Prestamo


class PrestamoRepository:
    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def get_all(self) -> Sequence[Prestamo]:
        return self.session.exec(select(Prestamo)).all()

    def get_by_id(self, prestamo_id: int) -> Optional[Prestamo]:
        return self.session.get(Prestamo, prestamo_id)

    def get_activos_by_socio(self, socio_id: int) -> Sequence[Prestamo]:
        statement = select(Prestamo).where(
            Prestamo.socio_id == socio_id,
            Prestamo.fecha_devolucion == None,
        )
        return self.session.exec(statement).all()

    def get_by_socio(self, socio_id: int, activos: Optional[bool] = None) -> Sequence[Prestamo]:
        query = select(Prestamo).where(Prestamo.socio_id == socio_id)
        if activos is True:
            query = query.where(Prestamo.fecha_devolucion == None)
        elif activos is False:
            query = query.where(Prestamo.fecha_devolucion != None)
        return self.session.exec(query).all()

    def save(self, prestamo: Prestamo) -> Prestamo:
        self.session.add(prestamo)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo