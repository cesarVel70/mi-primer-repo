from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente
from schemas import ClienteCreate, ClienteResponse
from typing import List

router = APIRouter(prefix='/api/v1/clientes', tags=['Clientes'])

@router.get('', response_model=List[ClienteResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@router.get('/{cliente_id}', response_model=ClienteResponse)
def obtener(cliente_id: int, db: Session = Depends(get_db)):
    c = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not c:
        raise HTTPException(404, 'Cliente no encontrado')
    return c

@router.post('', response_model=ClienteResponse)
def crear(data: ClienteCreate, db: Session = Depends(get_db)):
    c = Cliente(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c
