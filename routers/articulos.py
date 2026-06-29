from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Articulo
from schemas import ArticuloCreate, ArticuloResponse
from typing import List

router = APIRouter(prefix='/api/v1/articulos', tags=['Artículos'])

@router.get('', response_model=List[ArticuloResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Articulo).all()

@router.get('/{articulo_id}', response_model=ArticuloResponse)
def obtener(articulo_id: int, db: Session = Depends(get_db)):
    a = db.query(Articulo).filter(Articulo.id == articulo_id).first()
    if not a:
        raise HTTPException(404, 'Artículo no encontrado')
    return a

@router.post('', response_model=ArticuloResponse)
def crear(data: ArticuloCreate, db: Session = Depends(get_db)):
    a = Articulo(**data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a
