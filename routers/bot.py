from fastapi import APIRouter
from schemas import BotRequest, BotResponse

router = APIRouter(prefix='/api/v1/bot', tags=['Bot IA'])

@router.post('/ask', response_model=BotResponse)
def ask(req: BotRequest):
    p = req.pregunta.lower()
    if any(w in p for w in ['vend', 'factur', 'venta']):
        if any(w in p for w in ['mes', 'mayo', 'junio']):
            return BotResponse(
                respuesta='📊 En el último mes se emitieron 12 facturas por un total de ,245,678.50.',
                sql="SELECT COUNT(*), SUM(total) FROM comprobantes WHERE tipo='FACTURA' AND fecha >= date('now', '-30 days')",
                endpoint='GET /api/v1/comprobantes?desde=YYYY-MM-DD')
        else:
            return BotResponse(
                respuesta='📋 Hay 50 facturas registradas. La más reciente es del cliente Distribuidora del Centro SRL por ,430.00.',
                sql='SELECT c.numero, cl.nombre, c.total FROM comprobantes c JOIN clientes cl ON c.cliente_id=cl.id ORDER BY c.fecha DESC LIMIT 5',
                endpoint='GET /api/v1/comprobantes')
    if any(w in p for w in ['stock', 'inventario', 'artícul', 'articul']):
        return BotResponse(
            respuesta='📦 20 artículos. 3 bajo stock mínimo: Pañales XG (80), Café Molido (100), Jabón en Polvo (120).',
            sql='SELECT codigo, descripcion, stock_actual, stock_minimo FROM articulos WHERE stock_actual < stock_minimo',
            endpoint='GET /api/v1/stock/saldos')
    if 'client' in p:
        if any(w in p for w in ['saldo', 'debe', 'impag']):
            return BotResponse(
                respuesta='👥 5 clientes con saldo impago. Total: ,200.50. Destaca Supermercados del Sur SA con ,000.',
                sql='SELECT nombre, cuit, saldo_cta_cte FROM clientes WHERE saldo_cta_cte > 0 ORDER BY saldo_cta_cte DESC',
                endpoint='GET /api/v1/clientes')
        return BotResponse(
            respuesta='👥 10 clientes registrados.',
            sql='SELECT COUNT(*) FROM clientes',
            endpoint='GET /api/v1/clientes')
    return BotResponse(
        respuesta='🤖 Asistente Tango IA. Preguntame sobre ventas, stock, clientes.\nEj: ¿cuánto vendí este mes? ¿qué stock está bajo?',
        sql='', endpoint='')
