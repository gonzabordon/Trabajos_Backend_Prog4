from typing import List, Optional
from pydantic import BaseModel

class Pelicula(BaseModel):
    id : int
    titulo : str
    director : str
    genero : str
    anio : int
    en_stock : bool = True

class PeliculaUpdate(BaseModel):
    titulo : Optional[str] = None
    director : Optional[str] = None
    genero : Optional[str] = None
    anio : Optional[int] = None
    en_stock : Optional[bool] = None

class GetPeliculaResponse(BaseModel):
    peliculas : List[Pelicula]

class CreatePeliculaResponse(BaseModel):
    message : str

class UpdatePeliculaResponse(BaseModel):
    message : str

class DeletePeliculaResponse(BaseModel):
    message : str