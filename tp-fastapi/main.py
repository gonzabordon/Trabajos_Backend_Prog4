from typing import Optional, List
from fastapi import FastAPI, Query, status, HTTPException
from models.users import ( 
    User, 
    UserUpdate,
    GetUserResponse, 
    CreateUserResponse, 
    DeleteUserResponse, 
    UpdateUserResponse
)
from models.peliculas import (
    Pelicula,
    PeliculaUpdate,
    GetPeliculaResponse,
    CreatePeliculaResponse,
    DeletePeliculaResponse,
    UpdatePeliculaResponse
)

# Create the application instance
app = FastAPI()

usuarios : List[User] = [
    User(id = 1, name = "Panchito Vlasic"),
    User(id = 2, name = "Marquitos Vlasic")
]

peliculas: List[Pelicula] = [
    Pelicula(id=1, titulo="Django Sin Cadenas", director="Quentin Tarantino", genero="Accion", anio=2012),
    Pelicula(id=2, titulo="Interestelar", director="Christopher Nolan", genero="Ciencia Ficcion", anio=2014)
]

# Define a GET route for the root URL
@app.get("/")
def read_root():
    mensaje = "Trabajo Practico de FastAPI"
    return {"message": mensaje}

# Endpoint GET_USERS con filtrado opcional por estado (is_active)
@app.get("/user")
def get_users(
    is_active: Optional[bool] = Query(None, description="Filtrar por estado: True (activos), False (inactivos), o sin parámetro (todos)")
) -> GetUserResponse:
    if is_active is not None:
        filtered_users = [u for u in usuarios if u.is_active == is_active]
    else:
        filtered_users = usuarios
    return GetUserResponse(users=filtered_users)

# Enpoint DELETE_USER
@app.delete("/user/{id}")
def delete_user(id:int) -> DeleteUserResponse:
    for user in usuarios:
        if user.id == id:
            usuarios.remove(user)
            return {"message": "Usuario borrado"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )        

# Endpoint PUT/PATCH_USER para modificar los datos de un usuario existente
@app.put("/user/{id}")
def update_user(id: int, user_update: UserUpdate) -> UpdateUserResponse:
    for user in usuarios:
        if user.id == id:
            # Actualizamos solo los campos que vengan con valor (no nulos)
            if user_update.name is not None:
                user.name = user_update.name
            if user_update.is_active is not None:
                user.is_active = user_update.is_active
            return {"message": "Usuario modificado exitosamente"}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )

# Endpoint POST_USER
@app.post("/user")
def create_user(user:User) -> CreateUserResponse:
    usuarios.append(user)
    return {"message": "Usuario creado"} 

#-------------------------------------------------------------------------------------#

# Endpoint GET_PELICULAS con filtrado opcional por estado del stock (en_stock)
@app.get("/pelicula")
def get_peliculas(
    en_stock: Optional[bool] = Query(None, description="Filtrar por estado: True (hay existencias), False (no hay existencias), o sin parámetro (todas)")
) -> GetPeliculaResponse:
    if en_stock is not None:
        filtered_peliculas = [p for p in peliculas if p.en_stock == en_stock]
    else:
        filtered_peliculas = peliculas
    return GetPeliculaResponse(peliculas=filtered_peliculas)

# Endpoint GET_PELICULA_BY_ID
@app.get("/pelicula/{pelicula_id}")
def get_pelicula_by_id(pelicula_id:int) -> Pelicula:
    for pelicula in peliculas:
        if pelicula.id == pelicula_id:
            return pelicula
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Película no encontrada"
    )

# Enpoint DELETE_PELICULA
@app.delete("/pelicula/{id}")
def delete_pelicula(id:int) -> DeletePeliculaResponse:
    for pelicula in peliculas:
        if pelicula.id == id:
            peliculas.remove(pelicula)
            return {"message": "Pelicula borrada"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Pelicula no encontrada"
    )    

# Endpoint PUT_PELICULA para modificar los datos de una pelicula existente
@app.put("/pelicula/{id}")
def update_pelicula(id: int, pelicula_update: PeliculaUpdate) -> UpdatePeliculaResponse:
    for pelicula in peliculas:
        if pelicula.id == id:
            # Actualizamos solo los campos que vengan con valor (no nulos)
            if pelicula_update.titulo is not None:
                pelicula.titulo = pelicula_update.titulo
            if pelicula_update.director is not None:
                pelicula.director = pelicula_update.director
            if pelicula_update.genero is not None:
                pelicula.genero = pelicula_update.genero
            if pelicula_update.anio is not None:
                pelicula.anio = pelicula_update.anio
            if pelicula_update.en_stock is not None:
                pelicula.en_stock = pelicula_update.en_stock
            return {"message": "Pelicula modificada exitosamente"}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Pelicula no encontrada"
    )

# Endpoint POST_PELICULA
@app.post("/pelicula")
def create_pelicula(pelicula:Pelicula) -> CreatePeliculaResponse:
    peliculas.append(pelicula)
    return {"message": "Pelicula Agregada"} 