from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func,JSON
from app.db.database import Base


class Producto(Base):
    __tablename__ = "tbl_productos"
    id = Column(Integer,primary_key=True, index=True)
    codigo = Column(String(50),unique=True,index=True,nullable=False)
    nombre = Column(String(100),nullable=False)
    pais_origen = Column(String(100),nullable=False)
    descripcion = Column(Text,nullable=True)

    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    gramos = Column(Integer, nullable=True, default=0)

    calificacion = Column(Float, nullable=True, default=0.0)
    numero_opiniones = Column(Integer, nullable=True, default=0)

    # JSON stored as TEXT
    tipo_molienda = Column(JSON, nullable=True)
    imagenes = Column(JSON, nullable=True)
    categorias = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Pedido(Base):
    __tablename__ = "tbl_pedidos"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Float, nullable=False)
    cliente = Column(JSON, nullable=False)
    estado = Column(String(15), nullable=False)
    data = Column(JSON, nullable=False)
