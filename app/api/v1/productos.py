from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Producto
from app.schemas.schemas import ProductoCreate, ProductoOut, ProductoUpdate
from app.utils.json_tools import encode_json, decode_json
from app.core.security import require_auth, require_admin

router = APIRouter()

@router.get("/", response_model=dict, tags=["productos"])
def listar_productos(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    total = db.query(Producto).count()
    items = db.query(Producto).offset((page - 1) * limit).limit(limit).all()

    def to_dict(p: Producto):
        return {
            "id": p.id,
            "codigo": p.codigo,
            "nombre": p.nombre,
            "pais_origen":p.pais_origen,
            "descripcion": p.descripcion,
            "precio": p.precio,
            "stock": p.stock,
            "gramos": p.gramos,
            "calificacion": p.calificacion,
            "numero_opiniones": p.numero_opiniones,
            "tipo_molienda": decode_json(p.tipo_molienda),
            "imagenes": decode_json(p.imagenes),
            "categorias": decode_json(p.categorias),
            "created_at": p.created_at
        }
    return {"pagina": page, "limite": limit, "total": total, "items": [to_dict(x) for x in items]}

@router.get("/{id}", response_model=ProductoOut, tags=["productos"])
def obtener_producto(id: int, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    out = {
        **ProductoOut.model_validate(p).model_dump(),
        "tipo_molienda": decode_json(p.tipo_molienda),
        "imagenes": decode_json(p.imagenes),
        "categorias": decode_json(p.categorias)
    }
    return out

@router.post("/", response_model=ProductoOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)], tags=["productos"])
def crear_producto(payload: ProductoCreate, db: Session = Depends(get_db)):
    p = Producto(
        codigo=payload.codigo,
        nombre=payload.nombre,
        pais_origen=payload.pais_origen,
        descripcion=payload.descripcion,
        precio=payload.precio,
        stock=payload.stock,
        gramos=payload.gramos,
        calificacion=payload.calificacion,
        numero_opiniones=payload.numero_opiniones,
        tipo_molienda=payload.tipo_molienda,
        imagenes=payload.imagenes,
        categorias=payload.categorias
    )
    db.add(p)
    try:
        db.commit()
        db.refresh(p)
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear producto")
    return ProductoOut.model_validate(p)

@router.put("/{id}", response_model=ProductoOut, dependencies=[Depends(require_admin)], tags=["productos"])
def actualizar_producto(id: int, payload: ProductoCreate, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for k, v in payload.model_dump().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return ProductoOut.model_validate(p)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_auth)], tags=["productos"])
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(p)
    db.commit()
    return
