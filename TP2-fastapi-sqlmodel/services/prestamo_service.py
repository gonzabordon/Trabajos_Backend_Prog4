from datetime import date, timedelta
from sqlmodel import Session, select
from fastapi import HTTPException, status
from models.prestamo import Prestamo
from models.socio import Socio
from models.libro import Libro

def listar_prestamos(session: Session) -> list[Prestamo]:
    return session.exec(select(Prestamo)).all()

def registrar_prestamo(session: Session, socio_id: int, libro_id: int) -> Prestamo:
    # Regla 7: Socio inexistente
    socio = session.get(Socio, socio_id)
    if not socio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")

    # Regla 3: Socio inactivo no puede pedir préstamos (403)
    if not socio.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El socio está inactivo")

    # Regla 7: Libro inexistente
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")

    # Regla 2: No se presta un libro sin stock (409)
    if libro.stock <= 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro no tiene stock disponible")

    # Regla 1: Un socio no puede tener más de 3 préstamos activos (409)
    statement = select(Prestamo).where(Prestamo.socio_id == socio_id, Prestamo.fecha_devolucion == None)
    prestamos_activos = session.exec(statement).all()
    if len(prestamos_activos) >= 3:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El socio ya tiene 3 préstamos activos")

    # Regla 4: Plazo de 14 días
    hoy = date.today()
    vencimiento = hoy + timedelta(days=14)

    prestamo = Prestamo(
        socio_id=socio_id,
        libro_id=libro_id,
        fecha_prestamo=hoy,
        fecha_vencimiento=vencimiento,
        fecha_devolucion=None,
        multa=0.0
    )

    # Descontar stock
    libro.stock -= 1

    session.add(prestamo)
    session.add(libro)
    session.commit()
    session.refresh(prestamo)
    return prestamo

def registrar_devolucion(session: Session, prestamo_id: int) -> Prestamo:
    # Regla 7: Préstamo inexistente
    prestamo = session.get(Prestamo, prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado")

    # Regla 6: No se puede devolver un préstamo ya devuelto (409)
    if prestamo.fecha_devolucion is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El préstamo ya fue devuelto")

    hoy = date.today()
    prestamo.fecha_devolucion = hoy

    # Regla 5: Calcular multa ($100 x días de atraso)
    if hoy > prestamo.fecha_vencimiento:
        dias_atraso = (hoy - prestamo.fecha_vencimiento).days
        prestamo.multa = float(dias_atraso * 100)
    else:
        prestamo.multa = 0.0

    # Reponer stock
    libro = session.get(Libro, prestamo.libro_id)
    if libro:
        libro.stock += 1
        session.add(libro)

    session.add(prestamo)
    session.commit()
    session.refresh(prestamo)
    return prestamo