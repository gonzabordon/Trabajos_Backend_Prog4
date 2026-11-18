from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database import get_session
from models.libro import Libro, LibroCreate
from services import libro_service

router = APIRouter()

@router.get("/", response_model=list[Libro])
def listar_libros(disponibles: Optional[bool] = None, session: Session = Depends(get_session)):
    return libro_service.listar_libros(session, disponibles)

@router.post("/", response_model=Libro, status_code=status.HTTP_201_CREATED)
def create_libro(libro: LibroCreate, session: Session = Depends(get_session)):
    return libro_service.create_libro(session, libro)

@router.get("/{id}", response_model=Libro)
def get_libro(id: int, session: Session = Depends(get_session)):
    return libro_service.get_libro(session, id)

@router.put("/{id}", response_model=Libro)
def update_libro(id: int, libro_data: LibroCreate, session: Session = Depends(get_session)):
    return libro_service.update_libro(session, id, libro_data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_libro(id: int, session: Session = Depends(get_session)):
    libro_service.delete_libro(session, id)
    return None

@router.post("/{id}/autores/{autor_id}", status_code=status.HTTP_201_CREATED)
def asociar_autor(id: int, autor_id: int, session: Session = Depends(get_session)):
    return libro_service.asociar_autor_a_libro(session, id, autor_id)