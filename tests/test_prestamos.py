from datetime import date, timedelta
from fastapi import status
from models.prestamo import Prestamo

def test_listar_prestamos(client):
    res = client.get("/prestamos/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == []

def test_prestamo_exitoso_y_devolucion_a_tiempo(client):
    libro_id = client.post("/libros/", json={"titulo": "Clean Code", "isbn": "555", "stock": 2, "anio": 2008}).json()["id"]
    socio_id = client.post("/socios/", json={"nombre": "Pedro", "email": "pedro@mail.com", "activo": True}).json()["id"]

    # Regla 4: Plazo de 14 días
    res_prestamo = client.post("/prestamos/", json={"socio_id": socio_id, "libro_id": libro_id})
    assert res_prestamo.status_code == status.HTTP_201_CREATED
    prestamo_data = res_prestamo.json()
    f_prestamo = date.fromisoformat(prestamo_data["fecha_prestamo"])
    f_vencimiento = date.fromisoformat(prestamo_data["fecha_vencimiento"])
    assert (f_vencimiento - f_prestamo).days == 14

    # Verificar descuento de stock
    assert client.get(f"/libros/{libro_id}").json()["stock"] == 1

    # Regla 5: Devolución a tiempo (multa = 0) y reposición de stock
    prestamo_id = prestamo_data["id"]
    res_devolucion = client.post(f"/prestamos/{prestamo_id}/devolucion")
    assert res_devolucion.status_code == status.HTTP_200_OK
    assert res_devolucion.json()["multa"] == 0.0
    assert client.get(f"/libros/{libro_id}").json()["stock"] == 2

    # Regla 6: No se puede devolver un préstamo ya devuelto (409)
    res_re_devolucion = client.post(f"/prestamos/{prestamo_id}/devolucion")
    assert res_re_devolucion.status_code == status.HTTP_409_CONFLICT

def test_devolucion_con_atraso_calcula_multa(client, session):
    libro_id = client.post("/libros/", json={"titulo": "Refactoring", "isbn": "556", "stock": 1, "anio": 2018}).json()["id"]
    socio_id = client.post("/socios/", json={"nombre": "Laura", "email": "laura@mail.com", "activo": True}).json()["id"]

    prestamo_id = client.post("/prestamos/", json={"socio_id": socio_id, "libro_id": libro_id}).json()["id"]

    # Simular 5 días de atraso modificando la fecha de vencimiento en la base
    prestamo_db = session.get(Prestamo, prestamo_id)
    prestamo_db.fecha_vencimiento = date.today() - timedelta(days=5)
    session.add(prestamo_db)
    session.commit()

    # Regla 5: $100 x 5 días = $500
    res_devolucion = client.post(f"/prestamos/{prestamo_id}/devolucion")
    assert res_devolucion.status_code == status.HTTP_200_OK
    assert res_devolucion.json()["multa"] == 500.0
    assert client.get(f"/libros/{libro_id}").json()["stock"] == 1

def test_devolucion_prestamo_inexistente(client):
    assert client.post("/prestamos/999/devolucion").status_code == status.HTTP_404_NOT_FOUND

def test_prestamo_recursos_inexistentes(client):
    socio_id = client.post("/socios/", json={"nombre": "Ana", "email": "ana@mail.com", "activo": True}).json()["id"]
    libro_id = client.post("/libros/", json={"titulo": "DDD", "isbn": "557", "stock": 1, "anio": 2003}).json()["id"]

    assert client.post("/prestamos/", json={"socio_id": 999, "libro_id": libro_id}).status_code == status.HTTP_404_NOT_FOUND
    assert client.post("/prestamos/", json={"socio_id": socio_id, "libro_id": 999}).status_code == status.HTTP_404_NOT_FOUND

def test_prestamo_sin_stock(client):
    libro_id = client.post("/libros/", json={"titulo": "Libro Escaso", "isbn": "666", "stock": 0, "anio": 2021}).json()["id"]
    socio_id = client.post("/socios/", json={"nombre": "Lucia", "email": "lucia@mail.com", "activo": True}).json()["id"]

    assert client.post("/prestamos/", json={"socio_id": socio_id, "libro_id": libro_id}).status_code == status.HTTP_409_CONFLICT

def test_socio_inactivo_no_puede_prestar(client):
    libro_id = client.post("/libros/", json={"titulo": "Libro Normal", "isbn": "777", "stock": 5, "anio": 2021}).json()["id"]
    socio_id = client.post("/socios/", json={"nombre": "Carlos", "email": "carlos@mail.com", "activo": False}).json()["id"]

    assert client.post("/prestamos/", json={"socio_id": socio_id, "libro_id": libro_id}).status_code == status.HTTP_403_FORBIDDEN

def test_limite_tres_prestamos_activos(client):
    socio_id = client.post("/socios/", json={"nombre": "Martin", "email": "martin@mail.com", "activo": True}).json()["id"]

    libro_ids = []
    for i in range(4):
        res_l = client.post("/libros/", json={"titulo": f"Libro {i}", "isbn": f"888{i}", "stock": 5, "anio": 2020})
        libro_ids.append(res_l.json()["id"])

    for i in range(3):
        assert client.post("/prestamos/", json={"socio_id": socio_id, "libro_id": libro_ids[i]}).status_code == status.HTTP_201_CREATED

    # El 4to préstamo activo debe fallar con 409
    assert client.post("/prestamos/", json={"socio_id": socio_id, "libro_id": libro_ids[3]}).status_code == status.HTTP_409_CONFLICT