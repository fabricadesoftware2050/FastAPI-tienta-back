from fastapi import APIRouter, HTTPException,status

from app.core.security import create_access_token
from app.schemas.schemas import Token, LoginData

router = APIRouter()

#usuario admin fijo
my_admin = {
    "name":"Chris Gámez",
    "role":"admin",
    "email":"admin@gmail.com",
    "password":"Pa$$2050"
}

#usuario común fijo
my_customer = {
    "name":"Carlos Meza",
    "role":"client",
    "email":"client@gmail.com",
    "password":"Pa$$2050"
}

@router.post("/login",tags=["auth"],response_model=Token)
def login(datos: LoginData):
    if datos.email == my_admin["email"] and datos.password == my_admin["password"]:
        access_token = create_access_token({"sub": my_admin["email"], "name": my_admin["name"], "role": my_admin["role"]})
        return {"access_token":access_token,"token_type":"bearer"}
    elif datos.email == my_customer["email"] and datos.password == my_customer["password"]:
        access_token = create_access_token(
            {"sub": my_customer["email"], "name": my_customer["name"], "role": my_customer["role"]})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Credenciales incorrectas")
