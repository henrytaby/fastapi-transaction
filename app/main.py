from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.customers import routes as Customers
from app.db import create_db_and_tables
from app.plans import routes as Plans
from app.transactions import routes as Transactions

# ...existing code...
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import logging
import os
from datetime import datetime





version = "v1"

description = """
API de un Sistema de transacción, usando FastApi con Python.
UAB

This REST API is able to;
- Crear, Leer, Actualizar y eliminar Customers, Plans y Transactions
- Añadir relación de Customers con Planes, de Customers con Transacciones

    """

version_prefix = f"/api/{version}"

app = FastAPI(
    lifespan=create_db_and_tables,
    # lifespan=life_spna,
    title="AppTransactionFastAPI",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Henry Alejandro Taby Zenteno",
        "url": "https://github.com/henrytaby",
        "email": "henry.taby@gmail.com",
    },
    # openapi_url=f"{version_prefix}/openapi.json",
    # docs_url=f"{version_prefix}/docs",
    # redoc_url=f"{version_prefix}/redoc",
    openapi_tags=[
        {
            "name": "Customers",
            "description": "Funcionalidades que se tiene para realizar con el cliente (Customer)",
        },
        {
            "name": "Transactions",
            "description": "Todas las transacciones realizadas por el cliente (Customer)",
        },
        {
            "name": "Plans",
            "description": "Lista de planes relacionados al cliente (Customer)",
        },
        {
            "name": "Clientes",
            "description": "Lista de clientes",
        },
        {
            "name": "Docentes",
            "description": "Lista de clientes",
        },
        {
            "name": "Materias",
            "description": "Lista de clientes",
        },
    ],
)


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(log_type: str):
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(LOG_DIR, f"{log_type}_customer_{today}.log")
    logger = logging.getLogger(log_path)
    if not logger.hasHandlers():
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Convierte los errores para que sean serializables
    errors = exc.errors()
    for error in errors:
        if "ctx" in error and "error" in error["ctx"]:
            error["ctx"]["error"] = str(error["ctx"]["error"])
    error_logger = get_logger("error")
    error_logger.error(f"Validation error: {errors} | Body: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={"detail": errors, "body": exc.body},
    )


app.include_router(Customers.router, prefix="/customers", tags=["Customers"])
app.include_router(Transactions.router, prefix="/transaction", tags=["Transactions"])
app.include_router(Plans.router, prefix="/plans", tags=["Plans"])



"""
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time:.4f} seconds")
    return response


@app.middleware("http") 
async def log_request_headers(request: Request, call_next):
    print("Request Headers:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")
    response = await call_next(request) 
    return response
"""

security = HTTPBasic()


@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username == "admin" and credentials.password == "123":
        return {"message": f"Hola, Mundo {credentials.username}!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/name/{name}")
async def get_name(name: str):
    return {"message": f"Hola desarrollador: , {name}!"}


@app.get("/curso/{name}")
async def get_name(name: str):
    return {"message": f"El curso es de: , {name}!"}

"""
country_timezones = {
    "CO" : "America/Bogota",z
    "MX" : "America/Mexico_City",
    "AR" : "America/Argentina/Buenos_Aires",
    "BR" : "America/Sao_Paulo",
    "PE" : "America/Lima",
}





@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
    return invoice_data


@app.get('/time/{iso_code}')
async def get_time_by_iso(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    now = datetime.now(tz)
    #return {"datetime": now.strftime('%Y-%m-%d %H:%M:%S')}
    return {"datetime": now}

"""

