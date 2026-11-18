from fastapi import status

def test_crear_y_obtener_libro(client):
    response = client.post("/libros/", json={"titulo": "Cien años de soledad", "isbn": "978-0307474728", "stock": 5, "anio": 1967})
    assert response.status_code == status.HTTP_201_CREATED
    libro_id = response.json()["id"]

    res_get = client.get(f"/libros/{libro_id}")
    assert res_get.status_code == status.HTTP_200_OK
    assert res_get.json()["titulo"] == "Cien años de soledad"

    res_404 = client.get("/libros/999")
    assert res_404.status_code == status.HTTP_404_NOT_FOUND

def test_isbn_duplicado_libro(client):
    client.post("/libros/", json={"titulo": "Libro A", "isbn": "111111", "stock": 2, "anio": 2020})
    response = client.post("/libros/", json={"titulo": "Libro B", "isbn": "111111", "stock": 3, "anio": 2021})
    assert response.status_code == status.HTTP_409_CONFLICT

def test_listar_libros_y_disponibles(client):
    client.post("/libros/", json={"titulo": "Disponible", "isbn": "111", "stock": 2, "anio": 2020})
    client.post("/libros/", json={"titulo": "Agotado", "isbn": "222", "stock": 0, "anio": 2021})

    res_todos = client.get("/libros/")
    assert res_todos.status_code == status.HTTP_200_OK
    assert len(res_todos.json()) == 2

    res_disp = client.get("/libros/?disponibles=true")
    assert res_disp.status_code == status.HTTP_200_OK
    libros = res_disp.json()
    assert len(libros) == 1
    assert libros[0]["titulo"] == "Disponible"

def test_actualizar_libro(client):
    l1 = client.post("/libros/", json={"titulo": "Libro 1", "isbn": "100", "stock": 1, "anio": 2020}).json()
    client.post("/libros/", json={"titulo": "Libro 2", "isbn": "200", "stock": 1, "anio": 2020})

    res_ok = client.put(f"/libros/{l1['id']}", json={"titulo": "Editado", "isbn": "100", "stock": 4, "anio": 2022})
    assert res_ok.status_code == status.HTTP_200_OK
    assert res_ok.json()["stock"] == 4

    # Intentar actualizar usando un ISBN ya existente (409)
    res_dup = client.put(f"/libros/{l1['id']}", json={"titulo": "Editado", "isbn": "200", "stock": 4, "anio": 2022})
    assert res_dup.status_code == status.HTTP_409_CONFLICT

    # Libro inexistente (404)
    res_404 = client.put("/libros/999", json={"titulo": "X", "isbn": "999", "stock": 1, "anio": 2020})
    assert res_404.status_code == status.HTTP_404_NOT_FOUND

def test_eliminar_libro(client):
    libro_id = client.post("/libros/", json={"titulo": "Borrar", "isbn": "300", "stock": 1, "anio": 2020}).json()["id"]

    res_del = client.delete(f"/libros/{libro_id}")
    assert res_del.status_code == status.HTTP_204_NO_CONTENT

    res_404 = client.delete(f"/libros/{libro_id}")
    assert res_404.status_code == status.HTTP_404_NOT_FOUND

def test_asociar_autor_a_libro(client):
    libro_id = client.post("/libros/", json={"titulo": "Rayuela", "isbn": "333", "stock": 4, "anio": 1963}).json()["id"]
    autor_id = client.post("/autores/", json={"nombre": "Julio Cortazar", "nacionalidad": "Argentina"}).json()["id"]

    # Asociación exitosa
    res_ok = client.post(f"/libros/{libro_id}/autores/{autor_id}")
    assert res_ok.status_code == status.HTTP_201_CREATED

    # Asociación duplicada (409)
    res_dup = client.post(f"/libros/{libro_id}/autores/{autor_id}")
    assert res_dup.status_code == status.HTTP_409_CONFLICT

    # Libro o autor inexistente (404)
    assert client.post(f"/libros/999/autores/{autor_id}").status_code == status.HTTP_404_NOT_FOUND
    assert client.post(f"/libros/{libro_id}/autores/999").status_code == status.HTTP_404_NOT_FOUND