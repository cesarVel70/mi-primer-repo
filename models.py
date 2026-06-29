from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, index=True)
    nombre = Column(String(200))
    cuit = Column(String(13))
    categoria_iva = Column(String(50), default="Responsable Inscripto")
    saldo_cta_cte = Column(Float, default=0.0)
    bonificacion = Column(Float, default=0.0)
    lista_precio = Column(String(50), default="Lista 1")
    direccion = Column(String(300), default="")
    telefono = Column(String(50), default="")
    email = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.now)

class Articulo(Base):
    __tablename__ = "articulos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, index=True)
    descripcion = Column(String(300))
    unidad_medida = Column(String(20), default="UNIDAD")
    precio_compra = Column(Float, default=0.0)
    precio_venta = Column(Float, default=0.0)
    stock_actual = Column(Float, default=0.0)
    stock_minimo = Column(Float, default=0.0)
    categoria = Column(String(100), default="")

class Comprobante(Base):
    __tablename__ = "comprobantes"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20))
    letra = Column(String(1))
    numero = Column(String(20), unique=True)
    fecha = Column(Date, default=date.today)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    subtotal = Column(Float, default=0.0)
    iva = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    cae = Column(String(50), default="")
    estado = Column(String(20), default="EMITIDO")
    created_at = Column(DateTime, default=datetime.now)
    cliente = relationship("Cliente")
    detalles = relationship("ComprobanteDetalle", back_populates="comprobante")

class ComprobanteDetalle(Base):
    __tablename__ = "comprobantes_detalle"
    id = Column(Integer, primary_key=True, index=True)
    comprobante_id = Column(Integer, ForeignKey("comprobantes.id"))
    articulo_id = Column(Integer, ForeignKey("articulos.id"))
    cantidad = Column(Float, default=1.0)
    precio_unitario = Column(Float, default=0.0)
    subtotal = Column(Float, default=0.0)
    comprobante = relationship("Comprobante", back_populates="detalles")
    articulo = relationship("Articulo")

class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"
    id = Column(Integer, primary_key=True, index=True)
    articulo_id = Column(Integer, ForeignKey("articulos.id"))
    tipo = Column(String(20))
    cantidad = Column(Float)
    comprobante_id = Column(Integer, ForeignKey("comprobantes.id"), nullable=True)
    fecha = Column(Date, default=date.today)
    observacion = Column(String(300), default="")
    articulo = relationship("Articulo")
