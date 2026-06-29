from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix='/api/v1')

class TokenRequest(BaseModel):
    username: str = 'admin'
    password: str = 'admin'

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

@router.post('/token', response_model=TokenResponse)
def login(req: TokenRequest):
    if req.username == 'admin' and req.password == 'admin':
        return TokenResponse(access_token='tango-token-simulado-2024')
    raise HTTPException(401, 'Usuario o contraseña incorrectos')
