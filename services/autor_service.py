from sqlmodel import Session, select
from fastapi import HTTPException, status
from models.autor import Autor, AutorCreate

def listar_autores(session: Session) -> list[Autor]:
    return session.exec(select(Autor)).all()

def create_autor(session: Session, autor_data: AutorCreate) -> Autor:
    autor = Autor.model_validate(autor_data)
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor

def get_autor(session: Session, autor_id: int) -> Autor:
    autor = session.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
    return autor

def update_autor(session: Session, autor_id: int, autor_data: AutorCreate) -> Autor:
    autor = get_autor(session, autor_id)
    autor.nombre = autor_data.nombre
    autor.nacionalidad = autor_data.nacionalidad
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor

def delete_autor(session: Session, autor_id: int) -> None:
    autor = get_autor(session, autor_id)
    session.delete(autor)
    session.commit()