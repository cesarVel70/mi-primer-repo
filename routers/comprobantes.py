from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Comprobante, ComprobanteDetalle, Articulo, MovimientoStock
from schemas import ComprobanteCreate, ComprobanteResponse
from typing import List
from datetime import date

router = APIRouter(prefix='/api/v1/comprobantes', tags=['Comprobantes'])

@router.get('', response_model=List[ComprobanteResponse])
def listar(desde: date = None, hasta: date = None, db: Session = Depends(get_db)):
    q = db.query(Comprobante)
    if desde:
        q = q.filter(Comprobante.fecha >= desde)
    if hasta:
        q = q.filter(Comprobante.fecha <= hasta)
    return q.order_by(Comprobante.fecha.desc()).all()

@router.get('/{comp_id}', response_model=ComprobanteResponse)
def obtener(comp_id: int, db: Session = Depends(get_db)):
    c = db.query(Comprobante).filter(Comprobante.id == comp_id).first()
    if not c:
        raise HTTPException(404, 'Comprobante no encontrado')
    return c

@router.post('', response_model=ComprobanteResponse)
def crear(data: ComprobanteCreate, db: Session = Depends(get_db)):
    subtotal = sum(d.cantidad * d.precio_unitario for d in data.detalles)
    iva = round(subtotal * 0.21, 2)
    total = round(subtotal + iva, 2)
    ultimo = db.query(Comprobante).count()
    comp = Comprobante(
        tipo=data.tipo, letra=data.letra,
        numero=f'0001-{str(ultimo+1).zfill(8)}',
        fecha=data.fecha, cliente_id=data.cliente_id,
        subtotal=subtotal, iva=iva, total=total, cae='', estado='EMITIDO'
    )
    db.add(comp)
    db.flush()
    for d in data.detalles:
        db.add(ComprobanteDetalle(comprobante_id=comp.id, articulo_id=d.articulo_id, cantidad=d.cantidad, precio_unitario=d.precio_unitario, subtotal=d.cantidad * d.precio_unitario))
        art = db.query(Articulo).filter(Articulo.id == d.articulo_id).first()
        if art:
            art.stock_actual -= d.cantidad
        db.add(MovimientoStock(articulo_id=d.articulo_id, tipo='SALIDA', cantidad=d.cantidad, comprobante_id=comp.id, fecha=data.fecha, observacion=f'Venta {comp.numero}'))
    db.commit()
    db.refresh(comp)
    return comp
