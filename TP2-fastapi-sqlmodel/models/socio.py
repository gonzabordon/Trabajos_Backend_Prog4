from typing import Optional
from sqlmodel import SQLModel, Field

class SocioBase(SQLModel):
    nombre: str
    email: str
    activo: bool = True

class Socio(SocioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)

class SocioCreate(SocioBase):
    pass