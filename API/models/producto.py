#necesitamos un import para crear una clase
from pydantic import BaseModel, Field
#librería para dejar algún campo opcional
from typing import Optional

class Producto(BaseModel):
    id_producto: Optional[int] = None
    nombre: str = Field(default="Nuevo producto", min_length=5, max_length=100)
    id_marca: int
    nombre_marca: Optional[str]
    precio: int = Field(gt=0)
    stock: int = Field(gt=0)