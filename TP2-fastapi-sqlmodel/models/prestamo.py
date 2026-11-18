from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Prestamo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    socio_id: int = Field(foreign_key="socio.id")
    libro_id: int = Field(foreign_key="libro.id")
    fecha_prestamo: date = Field(default_factory=date.today)
    fecha_vencimiento: date
    fecha_devolucion: Optional[date] = None
    multa: float = 0.0