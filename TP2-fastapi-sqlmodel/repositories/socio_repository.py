from typing import Annotated, Optional, Sequence
from fastapi import Depends
from sqlmodel import Session, select
from database import get_session
from models.socio import Socio


class SocioRepository:
    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def get_all(self) -> Sequence[Socio]:
        return self.session.exec(select(Socio)).all()

    def get_by_id(self, socio_id: int) -> Optional[Socio]:
        return self.session.get(Socio, socio_id)

    def get_by_email(self, email: str) -> Optional[Socio]:
        statement = select(Socio).where(Socio.email == email)
        return self.session.exec(statement).first()

    def save(self, socio: Socio) -> Socio:
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def delete(self, socio: Socio) -> None:
        self.session.delete(socio)
        self.session.commit()