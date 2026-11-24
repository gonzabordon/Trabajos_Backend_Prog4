from typing import Annotated, Optional, Sequence
from fastapi import Depends, HTTPException, status
from models.prestamo import Prestamo
from models.socio import Socio, SocioCreate
from repositories.prestamo_repository import PrestamoRepository
from repositories.socio_repository import SocioRepository


class SocioService:
    def __init__(
        self,
        socio_repo: Annotated[SocioRepository, Depends()],
        prestamo_repo: Annotated[PrestamoRepository, Depends()],
    ):
        self.socio_repo = socio_repo
        self.prestamo_repo = prestamo_repo

    def listar_socios(self) -> Sequence[Socio]:
        return self.socio_repo.get_all()

    def create_socio(self, socio_data: SocioCreate) -> Socio:
        if self.socio_repo.get_by_email(socio_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado",
            )
        socio = Socio.model_validate(socio_data)
        return self.socio_repo.save(socio)

    def get_socio(self, socio_id: int) -> Socio:
        socio = self.socio_repo.get_by_id(socio_id)
        if not socio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Socio no encontrado",
            )
        return socio

    def update_socio(self, socio_id: int, socio_data: SocioCreate) -> Socio:
        socio = self.get_socio(socio_id)
        socio_existente = self.socio_repo.get_by_email(socio_data.email)
        if socio_existente and socio_existente.id != socio_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado",
            )
        socio.nombre = socio_data.nombre
        socio.email = socio_data.email
        socio.activo = socio_data.activo
        return self.socio_repo.save(socio)

    def delete_socio(self, socio_id: int) -> None:
        socio = self.get_socio(socio_id)
        self.socio_repo.delete(socio)

    def listar_prestamos_socio(
        self, socio_id: int, activos: Optional[bool] = None
    ) -> Sequence[Prestamo]:
        self.get_socio(socio_id)
        return self.prestamo_repo.get_by_socio(socio_id, activos=activos)