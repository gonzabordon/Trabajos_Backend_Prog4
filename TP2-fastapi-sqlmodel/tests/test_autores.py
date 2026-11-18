from fastapi import status

def test_crear_y_obtener_autor(client):
    response = client.post("/autores/", json={"nombre": "Gabriel Garcia Marquez", "nacionalidad": "Colombiana"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nombre"] == "Gabriel Garcia Marquez"

    res_get = client.get(f"/autores/{data['id']}")
    assert res_get.status_code == status.HTTP_200_OK
    assert res_get.json()["nacionalidad"] == "Colombiana"

def test_listar_autores(client):
    client.post("/autores/", json={"nombre": "Autor 1", "nacionalidad": "Argentina"})
    client.post("/autores/", json={"nombre": "Autor 2", "nacionalidad": "Chilena"})
    response = client.get("/autores/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

def test_actualizar_autor(client):
    res_post = client.post("/autores/", json={"nombre": "Nombre Viejo", "nacionalidad": "Arg"})
    autor_id = res_post.json()["id"]

    res_put = client.put(f"/autores/{autor_id}", json={"nombre": "Nombre Nuevo", "nacionalidad": "Argentina"})
    assert res_put.status_code == status.HTTP_200_OK
    assert res_put.json()["nombre"] == "Nombre Nuevo"

    res_404 = client.put("/autores/999", json={"nombre": "X", "nacionalidad": "Y"})
    assert res_404.status_code == status.HTTP_404_NOT_FOUND

def test_eliminar_autor(client):
    res_post = client.post("/autores/", json={"nombre": "Borrar", "nacionalidad": "Arg"})
    autor_id = res_post.json()["id"]

    res_del = client.delete(f"/autores/{autor_id}")
    assert res_del.status_code == status.HTTP_204_NO_CONTENT

    res_404 = client.delete(f"/autores/{autor_id}")
    assert res_404.status_code == status.HTTP_404_NOT_FOUND

def test_autor_no_encontrado(client):
    response = client.get("/autores/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND