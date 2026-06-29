from datetime import date, timedelta
from database import SessionLocal, engine, Base
from models import Cliente, Articulo, Comprobante, ComprobanteDetalle, MovimientoStock
import random

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Cliente).count() > 0:
        db.close()
        return
    clientes_data = [
        {'codigo': 'CLI001', 'nombre': 'Distribuidora del Centro SRL', 'cuit': '30-12345678-9', 'saldo_cta_cte': 15000.0},
        {'codigo': 'CLI002', 'nombre': 'Almacenes Generales SA', 'cuit': '30-23456789-0', 'saldo_cta_cte': 0.0},
        {'codigo': 'CLI003', 'nombre': 'Comercial Norte SH', 'cuit': '20-34567890-1', 'saldo_cta_cte': 8500.50},
        {'codigo': 'CLI004', 'nombre': 'Supermercados del Sur SA', 'cuit': '30-45678901-2', 'saldo_cta_cte': 32000.0},
        {'codigo': 'CLI005', 'nombre': 'Farmacia San Jorge', 'cuit': '27-56789012-3', 'saldo_cta_cte': 4200.0},
        {'codigo': 'CLI006', 'nombre': 'Hotel Plaza Mayor', 'cuit': '30-67890123-4', 'saldo_cta_cte': 0.0},
        {'codigo': 'CLI007', 'nombre': 'Taller Mecanico El Rapido', 'cuit': '20-78901234-5', 'saldo_cta_cte': 1200.0},
        {'codigo': 'CLI008', 'nombre': 'Panaderia La Espiga de Oro', 'cuit': '27-89012345-6', 'saldo_cta_cte': 0.0},
        {'codigo': 'CLI009', 'nombre': 'Libreria Tecnica SA', 'cuit': '33-90123456-7', 'saldo_cta_cte': 9800.0},
        {'codigo': 'CLI010', 'nombre': 'Transportes del Oeste SRL', 'cuit': '30-01234567-8', 'saldo_cta_cte': 6500.0},
    ]
    clientes = [Cliente(**c) for c in clientes_data]
    db.add_all(clientes)
    db.flush()
    articulos_data = [
        {'codigo': 'ART001', 'descripcion': 'Harina de Trigo 0000 x 1kg', 'precio_compra': 80.0, 'precio_venta': 140.0, 'stock_actual': 500, 'stock_minimo': 50, 'categoria': 'ALIMENTOS'},
        {'codigo': 'ART002', 'descripcion': 'Aceite de Girasol x 1.5L', 'precio_compra': 180.0, 'precio_venta': 320.0, 'stock_actual': 300, 'stock_minimo': 30, 'categoria': 'ALIMENTOS'},
        {'codigo': 'ART003', 'descripcion': 'Arroz Largo Fino x 1kg', 'precio_compra': 120.0, 'precio_venta': 210.0, 'stock_actual': 400, 'stock_minimo': 40, 'categoria': 'ALIMENTOS'},
        {'codigo': 'ART004', 'descripcion': 'Leche Entera x 1L', 'precio_compra': 160.0, 'precio_venta': 280.0, 'stock_actual': 250, 'stock_minimo': 25, 'categoria': 'LACTEOS'},
        {'codigo': 'ART005', 'descripcion': 'Queso Cremoso x 500g', 'precio_compra': 250.0, 'precio_venta': 450.0, 'stock_actual': 150, 'stock_minimo': 15, 'categoria': 'LACTEOS'},
        {'codigo': 'ART006', 'descripcion': 'Yogur Natural x 200g', 'precio_compra': 90.0, 'precio_venta': 160.0, 'stock_actual': 200, 'stock_minimo': 20, 'categoria': 'LACTEOS'},
        {'codigo': 'ART007', 'descripcion': 'Detergente Lavavajillas x 500ml', 'precio_compra': 95.0, 'precio_venta': 170.0, 'stock_actual': 180, 'stock_minimo': 20, 'categoria': 'LIMPIEZA'},
        {'codigo': 'ART008', 'descripcion': 'Lavandina x 1L', 'precio_compra': 70.0, 'precio_venta': 130.0, 'stock_actual': 350, 'stock_minimo': 35, 'categoria': 'LIMPIEZA'},
        {'codigo': 'ART009', 'descripcion': 'Jabon en Polvo x 800g', 'precio_compra': 200.0, 'precio_venta': 360.0, 'stock_actual': 120, 'stock_minimo': 15, 'categoria': 'LIMPIEZA'},
        {'codigo': 'ART010', 'descripcion': 'Panales XG x 48u', 'precio_compra': 650.0, 'precio_venta': 1150.0, 'stock_actual': 80, 'stock_minimo': 10, 'categoria': 'PERFUMERIA'},
        {'codigo': 'ART011', 'descripcion': 'Shampoo Anticaspa x 300ml', 'precio_compra': 220.0, 'precio_venta': 400.0, 'stock_actual': 90, 'stock_minimo': 10, 'categoria': 'PERFUMERIA'},
        {'codigo': 'ART012', 'descripcion': 'Desodorante Spray x 150ml', 'precio_compra': 140.0, 'precio_venta': 260.0, 'stock_actual': 110, 'stock_minimo': 15, 'categoria': 'PERFUMERIA'},
        {'codigo': 'ART013', 'descripcion': 'Galletitas Dulces x 200g', 'precio_compra': 60.0, 'precio_venta': 110.0, 'stock_actual': 600, 'stock_minimo': 60, 'categoria': 'ALIMENTOS'},
        {'codigo': 'ART014', 'descripcion': 'Agua Mineral x 2L', 'precio_compra': 85.0, 'precio_venta': 150.0, 'stock_actual': 450, 'stock_minimo': 45, 'categoria': 'BEBIDAS'},
        {'codigo': 'ART015', 'descripcion': 'Gaseosa Cola x 1.5L', 'precio_compra': 130.0, 'precio_venta': 240.0, 'stock_actual': 350, 'stock_minimo': 35, 'categoria': 'BEBIDAS'},
        {'codigo': 'ART016', 'descripcion': 'Cerveza Rubia x 1L', 'precio_compra': 200.0, 'precio_venta': 380.0, 'stock_actual': 200, 'stock_minimo': 20, 'categoria': 'BEBIDAS'},
        {'codigo': 'ART017', 'descripcion': 'Arroz Integral x 1kg', 'precio_compra': 150.0, 'precio_venta': 270.0, 'stock_actual': 280, 'stock_minimo': 30, 'categoria': 'ALIMENTOS'},
        {'codigo': 'ART018', 'descripcion': 'Fideos Spaghetti x 500g', 'precio_compra': 75.0, 'precio_venta': 140.0, 'stock_actual': 500, 'stock_minimo': 50, 'categoria': 'ALIMENTOS'},
        {'codigo': 'ART019', 'descripcion': 'Azucar x 1kg', 'precio_compra': 100.0, 'precio_venta': 180.0, 'stock_actual': 400, 'stock_minimo': 40, 'categoria': 'ALIMENTOS'},
        {'codigo': 'ART020', 'descripcion': 'Cafe Molido x 250g', 'precio_compra': 350.0, 'precio_venta': 650.0, 'stock_actual': 100, 'stock_minimo': 10, 'categoria': 'ALIMENTOS'},
    ]
    articulos = [Articulo(**a) for a in articulos_data]
    db.add_all(articulos)
    db.flush()
    for i in range(50):
        dias_atras = random.randint(1, 60)
        c = random.choice(clientes)
        a = random.choice(articulos)
        cant = random.randint(1, 20)
        precio = a.precio_venta
        subt = round(cant * precio, 2)
        iva_val = round(subt * 0.21, 2)
        total = round(subt + iva_val, 2)
        comp = Comprobante(
            tipo='FACTURA', letra='B', numero=f'0001-{str(i+1).zfill(8)}',
            fecha=date.today() - timedelta(days=dias_atras),
            cliente_id=c.id, subtotal=subt, iva=iva_val, total=total,
            cae=str(random.randint(60000000000000, 69999999999999)), estado='EMITIDO'
        )
        db.add(comp)
        db.flush()
        db.add(ComprobanteDetalle(comprobante_id=comp.id, articulo_id=a.id, cantidad=cant, precio_unitario=precio, subtotal=subt))
        db.add(MovimientoStock(articulo_id=a.id, tipo='SALIDA', cantidad=cant, comprobante_id=comp.id, fecha=comp.fecha, observacion=f'Venta FACTURA {comp.numero}'))
    db.commit()
    db.close()
    print('Base de datos inicializada con datos de ejemplo.')
