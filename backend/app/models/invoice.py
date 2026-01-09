from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class InvoiceBase(SQLModel):
    invoice_number: str = Field(index=True)
    amount: float
    status: str = Field(default="unpaid", index=True)  # paid / unpaid
    issue_date: Optional[date] = None
    due_date: Optional[date] = None


class Invoice(InvoiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    document_id: Optional[int] = Field(default=None, foreign_key="document.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    project: Optional["Project"] = Relationship(back_populates="invoices")


class InvoiceCreate(InvoiceBase):
    project_id: int
    document_id: Optional[int] = None


class InvoiceRead(InvoiceBase):
    id: int
    project_id: int
    document_id: Optional[int]
    created_at: datetime


