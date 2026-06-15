from pydantic import BaseModel
from typing import Optional

class tarefacreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False

class tarefaresponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    concluida: bool
    model_config = {"from_attributes": True}