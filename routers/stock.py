from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Articulo, MovimientoStock

router = APIRouter(prefix='/api/v1/stock', tags=['Stock'])

@router.get('/saldos')
def saldos(db: Session = Depends(get_db)):
    articulos = db.query(Articulo).all()
    return [{'id': a.id, 'codigo': a.codigo, 'descripcion': a.descripcion, 'stock_actual': a.stock_actual, 'stock_minimo': a.stock_minimo, 'alerta': a.stock_actual < a.stock_minimo} for a in articulos]

@router.get('/movimientos')
def movimientos(articulo_id: int = None, db: Session = Depends(get_db)):
    q = db.query(MovimientoStock)
    if articulo_id:
        q = q.filter(MovimientoStock.articulo_id == articulo_id)
    return q.order_by(MovimientoStock.fecha.desc()).limit(100).all()
