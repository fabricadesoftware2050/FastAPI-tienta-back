from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.db.database import get_db
from app.models.models import Pedido
from app.schemas.schemas import PedidoCreate, PedidoOut

router = APIRouter()


@router.post("/", response_model=PedidoOut)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):

    # Convertimos items a dicts
    items_dict = [item.model_dump() for item in pedido.items]

    # Construimos el JSON que sí es serializable
    data_final = {
        "items": items_dict,
        "direccion": pedido.direccion,
        "metodo_pago": pedido.metodo_pago
    }

    nuevo = Pedido(
        total=pedido.total,
        cliente=pedido.cliente,
        estado="pendiente",
        data=data_final
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return PedidoOut.model_validate(nuevo)

