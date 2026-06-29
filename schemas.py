from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ClienteBase(BaseModel):
    codigo: str
    nombre: str
    cuit: str = ""
    categoria_iva: str = "Responsable Inscripto"
    saldo_cta_cte: float = 0.0
    bonificacion: float = 0.0
    lista_precio: str = "Lista 1"
    direccion: str = ""
    telefono: str = ""
    email: str = ""
class ClienteCreate(ClienteBase):
    pass
class ClienteResponse(ClienteBase):
    id: int
    class Config:
        from_attributes = True

class ArticuloBase(BaseModel):
    codigo: str
    descripcion: str
    unidad_medida: str = "UNIDAD"
    precio_compra: float = 0.0
    precio_venta: float = 0.0
    stock_actual: float = 0.0
    stock_minimo: float = 0.0
    categoria: str = ""
class ArticuloCreate(ArticuloBase):
    pass
class ArticuloResponse(ArticuloBase):
    id: int
    class Config:
        from_attributes = True

class ComprobanteDetalleCreate(BaseModel):
    articulo_id: int
    cantidad: float
    precio_unitario: float
class ComprobanteCreate(BaseModel):
    tipo: str = "FACTURA"
    letra: str = "B"
    cliente_id: int
    fecha: date = date.today()
    detalles: List[ComprobanteDetalleCreate]
class ComprobanteResponse(BaseModel):
    id: int
    tipo: str
    letra: str
    numero: str
    fecha: date
    cliente_id: Optional[int] = None
    subtotal: float
    iva: float
    total: float
    cae: str
    estado: str
    class Config:
        from_attributes = True

class BotRequest(BaseModel):
    pregunta: str
class BotResponse(BaseModel):
    respuesta: str
    sql: str = ""
    endpoint: str = ""
