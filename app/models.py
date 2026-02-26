from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr, field_validator
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, Session, SQLModel, select

from app.db import engine


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


"""
Customer Plan
------------------------------
"""


class CustomerPlan(SQLModel, table=True):
    __tablename__ = "customer_plan"
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )


"""
Plan
------------------------------
"""


class PlanBase(SQLModel):
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str | None = Field(default=None)


class PlanCreate(PlanBase):
    pass


class PlanUpdate(PlanBase):
    pass


class Plan(PlanBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    customers: list["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )


"""
CUSTOMER
------------------------------
"""


class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None, ge=18)

class CustomerCreate(CustomerBase):
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        result = session.exec(query).first()
        if result:
            raise ValueError("This email is already registered")
        return value

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list["Plan"] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )


"""
TRANSACTION
------------------------------
"""


class TransactionBase(SQLModel):
    ammount: int = Field(default=None)
    description: str = Field(default=None)


class TransactionCreate(TransactionBase):
    pass
    # customer_id: int = Field(foreign_key="customer.id")


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )


"""
INVOICE
------------------------------
"""
"""
class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)

"""
