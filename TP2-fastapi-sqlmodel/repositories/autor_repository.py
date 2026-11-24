from typing import Annotated, Optional, Sequence
from fastapi import Depends
from sqlmodel import Session, select
from database import get_session
from models.autor import Autor


class AutorRepository:
    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def get_all(self) -> Sequence[Autor]:
        return self.session.exec(select(Autor)).all()

    def get_by_id(self, autor_id: int) -> Optional[Autor]:
        return self.session.get(Autor, autor_id)

    def save(self, autor: Autor) -> Autor:
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def delete(self, autor: Autor) -> None:
        self.session.delete(autor)
        self.session.commit()