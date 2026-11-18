from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from models.libro_autor import LibroAutor

if TYPE_CHECKING:
    from models.autor import Autor

class LibroBase(SQLModel):
    titulo: str
    isbn: str
    stock: int = Field(ge=0)
    anio: int

class Libro(LibroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    isbn: str = Field(unique=True, index=True)
    autores: List["Autor"] = Relationship(back_populates="libros", link_model=LibroAutor)

class LibroCreate(LibroBase):
    pass