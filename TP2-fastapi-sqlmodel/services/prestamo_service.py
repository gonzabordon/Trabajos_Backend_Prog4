from datetime import date, timedelta
from typing import Annotated, Sequence
from fastapi import Depends, HTTPException, status
from models.prestamo import Prestamo
from repositories.libro_repository import LibroRepository
from repositories.prestamo_repository import PrestamoRepository
from repositories.socio_repository import SocioRepository


class PrestamoService:
    def __init__(
        self,
        prestamo_repo: Annotated[PrestamoRepository, Depends()],
        socio_repo: Annotated[SocioRepository, Depends()],
        libro_repo: Annotated[LibroRepository, Depends()],
    ):
        self.prestamo_repo = prestamo_repo
        self.socio_repo = socio_repo
        self.libro_repo = libro_repo

    def listar_prestamos(self) -> Sequence[Prestamo]:
        return self.prestamo_repo.get_all()

    def registrar_prestamo(self, socio_id: int, libro_id: int) -> Prestamo:
        # Regla 7: Socio inexistente
        socio = self.socio_repo.get_by_id(socio_id)
        if not socio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Socio no encontrado",
            )

        # Regla 3: Socio inactivo no puede pedir préstamos (403)
        if not socio.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El socio está inactivo",
            )

        # Regla 7: Libro inexistente
        libro = self.libro_repo.get_by_id(libro_id)
        if not libro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Libro no encontrado",
            )

        # Regla 2: No se presta un libro sin stock (409)
        if libro.stock <= 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El libro no tiene stock disponible",
            )

        # Regla 1: Un socio no puede tener más de 3 préstamos activos (409)
        prestamos_activos = self.prestamo_repo.get_activos_by_socio(socio_id)
        if len(prestamos_activos) >= 3:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El socio ya tiene 3 préstamos activos",
            )

        # Regla 4: Plazo de 14 días
        hoy = date.today()
        vencimiento = hoy + timedelta(days=14)

        prestamo = Prestamo(
            socio_id=socio_id,
            libro_id=libro_id,
            fecha_prestamo=hoy,
            fecha_vencimiento=vencimiento,
            fecha_devolucion=None,
            multa=0.0,
        )

        # Descontar stock y guardar
        libro.stock -= 1
        self.libro_repo.save(libro)
        return self.prestamo_repo.save(prestamo)

    def registrar_devolucion(self, prestamo_id: int) -> Prestamo:
        # Regla 7: Préstamo inexistente
        prestamo = self.prestamo_repo.get_by_id(prestamo_id)
        if not prestamo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Préstamo no encontrado",
            )

        # Regla 6: No se puede devolver un préstamo ya devuelto (409)
        if prestamo.fecha_devolucion is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El préstamo ya fue devuelto",
            )

        hoy = date.today()
        prestamo.fecha_devolucion = hoy

        # Regla 5: Calcular multa ($100 x días de atraso)
        if hoy > prestamo.fecha_vencimiento:
            dias_atraso = (hoy - prestamo.fecha_vencimiento).days
            prestamo.multa = float(dias_atraso * 100)
        else:
            prestamo.multa = 0.0

        # Reponer stock y guardar
        libro = self.libro_repo.get_by_id(prestamo.libro_id)
        if libro:
            libro.stock += 1
            self.libro_repo.save(libro)

        return self.prestamo_repo.save(prestamo)