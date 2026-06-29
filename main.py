from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader
from database import engine, Base
from seed import seed
from routers import auth, clientes, articulos, comprobantes, stock, bot, resumen
import os

app = FastAPI(title='Tango Gestión Prototype', version='1.0.0')

Base.metadata.create_all(bind=engine)
seed()

_templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
_jinja_env = Environment(loader=FileSystemLoader(_templates_dir))

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(articulos.router)
app.include_router(comprobantes.router)
app.include_router(stock.router)
app.include_router(resumen.router)
app.include_router(bot.router)

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse({'error': 'Endpoint no encontrado', 'docs': '/docs'}, status_code=404)

@app.get('/', response_class=HTMLResponse)
def dashboard(request: Request):
    template = _jinja_env.get_template('dashboard.html')
    return HTMLResponse(template.render({'request': request}))
