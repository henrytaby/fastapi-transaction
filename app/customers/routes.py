from fastapi import APIRouter, Query, status

from app.customers.service import CustomerService
from app.db import SessionDep
from app.models import (
    Customer,
    CustomerCreate,
    CustomerUpdate,
    StatusEnum,
    Transaction,
    TransactionCreate,
)

router = APIRouter()
service = CustomerService()


# CREATE
# ----------------------
@router.post(
    "/",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["Customers"],
)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    """
    Crea un nuevo cliente.
    Valida que el email no esté ya registrado.
    """
    return service.create_customer(customer_data, session)


# GET ONE
# ----------------------
@router.get("/{customer_id}", response_model=Customer, tags=["Customers"])
async def read_customer(customer_id: int, session: SessionDep):
    return service.read_customer(customer_id, session)


# UPDATE
# ----------------------
@router.patch(
    "/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED
)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    return service.update_customer(customer_id, customer_data, session)


# DELETE
# ----------------------
@router.delete("/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    return service.delete_customer(customer_id, session)


# GET ALL CUSTOMERS
# ----------------------
@router.get("/", response_model=list[Customer])
async def get_all_customers(session: SessionDep):
    data = service.get_all_customers(session)
    return data
    # return session.exec(select(Customer)).all()


# CREATE - CUSTOMER PLAN
# ----------------------
@router.post("/{customer_id}/plans/{plan_id}")
async def create_customer_plan(
    customer_id: int,
    plan_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query(),
):
    return service.create_customer_plan(customer_id, plan_id, session, plan_status)


# List All - Customer Plans
# ----------------------
@router.get("/{customer_id}/plans")
async def get_all_customer_plans(
    customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()
):
    """
    Devuelve todos los planes relacionos al usuario seleccionado,
    ademas se encuentra filtrado por su <b>estado <b/>
    """
    return service.get_all_customer_plans(customer_id, session, plan_status)


# CREATE - CUSTOMER TRANSACTION
# ----------------------
@router.post("/{customer_id}/transactions", response_model=Transaction)
async def create_customer_transaction(
    customer_id: int, transaction_data: TransactionCreate, session: SessionDep
):
    """
    Crea una transacción para el usuario seleccionado.
    """
    return service.create_customer_transaction(customer_id, transaction_data, session)


# GET All CUSTOMER TRANSACTIONS
# ----------------------
@router.get("/{customer_id}/transactions")
async def get_all_customer_transactions(customer_id: int, session: SessionDep):
    """
    Devuelve todas las transacciones realizadas por el usuario seleccionado
    """
    return service.get_all_customer_transactions(customer_id, session)
