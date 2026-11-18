from fastapi import status

def test_crear_y_obtener_socio(client):
    response = client.post("/socios/", json={"nombre": "Juan Perez", "email": "juan@mail.com", "activo": True})
    assert response.status_code == status.HTTP_201_CREATED
    socio_id = response.json()["id"]

    res_get = client.get(f"/socios/{socio_id}")
    assert res_get.status_code == status.HTTP_200_OK
    assert res_get.json()["nombre"] == "Juan Perez"

    assert client.get("/socios/999").status_code == status.HTTP_404_NOT_FOUND

def test_listar_socios(client):
    client.post("/socios/", json={"nombre": "Socio 1", "email": "s1@mail.com", "activo": True})
    client.post("/socios/", json={"nombre": "Socio 2", "email": "s2@mail.com", "activo": False})
    res = client.get("/socios/")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 2

def test_email_duplicado_socio(client):
    client.post("/socios/", json={"nombre": "Juan Perez", "email": "juan@mail.com", "activo": True})
    response = client.post("/socios/", json={"nombre": "Otro Juan", "email": "juan@mail.com", "activo": True})
    assert response.status_code == status.HTTP_409_CONFLICT

def test_actualizar_socio(client):
    s1 = client.post("/socios/", json={"nombre": "S1", "email": "s1@mail.com", "activo": True}).json()
    client.post("/socios/", json={"nombre": "S2", "email": "s2@mail.com", "activo": True})

    res_ok = client.put(f"/socios/{s1['id']}", json={"nombre": "S1 Edit", "email": "s1@mail.com", "activo": False})
    assert res_ok.status_code == status.HTTP_200_OK
    assert res_ok.json()["activo"] is False

    # Email duplicado al actualizar (409)
    res_dup = client.put(f"/socios/{s1['id']}", json={"nombre": "S1 Edit", "email": "s2@mail.com", "activo": True})
    assert res_dup.status_code == status.HTTP_409_CONFLICT

    # Socio inexistente (404)
    assert client.put("/socios/999", json={"nombre": "X", "email": "x@mail.com", "activo": True}).status_code == status.HTTP_404_NOT_FOUND

def test_eliminar_socio(client):
    socio_id = client.post("/socios/", json={"nombre": "Borrar", "email": "b@mail.com", "activo": True}).json()["id"]
    assert client.delete(f"/socios/{socio_id}").status_code == status.HTTP_204_NO_CONTENT
    assert client.delete(f"/socios/{socio_id}").status_code == status.HTTP_404_NOT_FOUND

def test_listar_prestamos_socio(client):
    socio_id = client.post("/socios/", json={"nombre": "Ana", "email": "ana@mail.com", "activo": True}).json()["id"]
    libro_id = client.post("/libros/", json={"titulo": "Libro Test", "isbn": "444", "stock": 5, "anio": 2022}).json()["id"]

    prestamo_id = client.post("/prestamos/", json={"socio_id": socio_id, "libro_id": libro_id}).json()["id"]
    client.post(f"/prestamos/{prestamo_id}/devolucion")

    # Histórico completo (1 préstamo devuelto)
    res_todos = client.get(f"/socios/{socio_id}/prestamos")
    assert res_todos.status_code == status.HTTP_200_OK
    assert len(res_todos.json()) == 1

    # Solo activos (0 activos)
    res_activos = client.get(f"/socios/{socio_id}/prestamos?activos=true")
    assert res_activos.status_code == status.HTTP_200_OK
    assert len(res_activos.json()) == 0

    # Socio inexistente (404)
    assert client.get("/socios/999/prestamos").status_code == status.HTTP_404_NOT_FOUND