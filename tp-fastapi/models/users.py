from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id : int
    name : str
    is_active : bool = True # default value field becomes optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class GetUserResponse(BaseModel):
    users : List[User]

class CreateUserResponse(BaseModel):
    message : str

class UpdateUserResponse(BaseModel):
    message: str

class DeleteUserResponse(BaseModel):
    message : str