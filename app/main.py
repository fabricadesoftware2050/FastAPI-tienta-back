from fastapi import FastAPI
from app.db.database import Base, engine
from app.core.cors import setup_cors
from app.api.v1 import productos, pedidos, auth


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Productos y Pedidos")

setup_cors(app)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(productos.router, prefix="/productos", tags=["productos"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["pedidos"])
