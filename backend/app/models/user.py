from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id:str
    email:str
    name:str
    picture: Optional[str]=None

