from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Comprobante, Cliente, Articulo
from datetime import date

router = APIRouter(prefix='/api/v1/resumen', tags=['Resumen'])

@router.get('')
def resumen(db: Session = Depends(get_db)):
    total_ventas = db.query(func.sum(Comprobante.total)).scalar() or 0
    ventas_mes = db.query(func.sum(Comprobante.total)).filter(func.strftime('%Y-%m', Comprobante.fecha) == date.today().strftime('%Y-%m')).scalar() or 0
    return {
        'total_ventas': round(total_ventas, 2),
        'ventas_mes': round(ventas_mes, 2),
        'cantidad_facturas': db.query(Comprobante).count(),
        'cantidad_clientes': db.query(Cliente).count(),
        'cantidad_articulos': db.query(Articulo).count(),
    }
