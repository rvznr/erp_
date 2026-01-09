from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, require_role
from app.models.invoice import Invoice, InvoiceCreate, InvoiceRead
from app.models.project import Project

router = APIRouter(prefix="/finance", tags=["finance"])


@router.post(
    "/invoices",
    response_model=InvoiceRead,
    dependencies=[Depends(require_role(["Admin", "Accountant"]))],
)
def create_invoice(invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == invoice_in.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    invoice = Invoice.from_orm(invoice_in)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/invoices", response_model=List[InvoiceRead])
def list_invoices(project_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Invoice)
    if project_id is not None:
        query = query.filter(Invoice.project_id == project_id)
    return query.order_by(Invoice.created_at.desc()).all()


