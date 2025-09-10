from __future__ import annotations
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Table, Column
from typing import List, Optional


# Creating our Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)

# Models
class Customers(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(30), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(db.String(100), unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    serviceTickets: Mapped[List['ServiceTickets']] = db.relationship(back_populates='customer')

# Association Table
ServiceMechanics = Table(
    "serviceMechanics",
    Base.metadata,
    Column("service_ticket_id", db.ForeignKey("serviceTickets.id")),
    Column("mechanic_id", db.ForeignKey("mechanics.id"))
)

class ServiceTickets(Base):
    __tablename__ = "serviceTickets"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    VIN: Mapped[str] = mapped_column(db.String(100), unique=True)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_desc: Mapped[str] = mapped_column(db.String(30), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    customer: Mapped['Customers'] = db.relationship(back_populates='serviceTickets')
    mechanics: Mapped[List['Mechanics']] = db.relationship(secondary=ServiceMechanics, back_populates='serviceTickets')


class Mechanics(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(30), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(db.String(100), unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    serviceTickets: Mapped[List['ServiceTickets']] = db.relationship(secondary=ServiceMechanics, back_populates='mechanics')
