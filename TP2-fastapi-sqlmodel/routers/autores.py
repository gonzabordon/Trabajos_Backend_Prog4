from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database import get_session
from models.autor import Autor, AutorCreate
from services import autor_service

router = APIRouter()

@router.get("/", response_model=list[Autor])
def listar_autores(session: Session = Depends(get_session)):
    return autor_service.listar_autores(session)

@router.post("/", response_model=Autor, status_code=status.HTTP_201_CREATED)
def create_autor(autor: AutorCreate, session: Session = Depends(get_session)):
    return autor_service.create_autor(session, autor)

@router.get("/{id}", response_model=Autor)
def get_autor(id: int, session: Session = Depends(get_session)):
    return autor_service.get_autor(session, id)

@router.put("/{id}", response_model=Autor)
def update_autor(id: int, autor_data: AutorCreate, session: Session = Depends(get_session)):
    return autor_service.update_autor(session, id, autor_data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_autor(id: int, session: Session = Depends(get_session)):
    autor_service.delete_autor(session, id)
    return None