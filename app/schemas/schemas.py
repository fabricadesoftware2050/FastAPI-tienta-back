from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

# Producto
class ProductoBase(BaseModel):
    codigo: str = Field(..., min_length=1)
    nombre: str
    pais_origen: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    gramos: Optional[int] = 0
    calificacion: Optional[float] = 0.0
    numero_opiniones: Optional[int] = 0
    tipo_molienda: Optional[List[str]] = None
    imagenes: Optional[List[str]] = None
    categorias: Optional[List[str]] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

# Pedido
class PedidoItem(BaseModel):
    producto_id: int
    nombre: str
    cantidad: int
    precio_unitario: float
    imagen_principal: str

class PedidoCreate(BaseModel):
    items: List[PedidoItem]
    direccion: Optional[str] = None
    metodo_pago: Optional[str] = None
    total : float
    cliente : str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PedidoOut(BaseModel):
    id: int
    fecha: datetime
    total: float
    cliente: str
    estado: str
    data: Dict[str, Any]

    model_config = {"from_attributes": True}


# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    email:str
    password:str
