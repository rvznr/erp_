from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.document import Document
from app.models.invoice import Invoice
from app.models.project import Project

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=Dict[str, Any])
def get_dashboard(db: Session = Depends(get_db)):
    total_budget = db.query(func.coalesce(func.sum(Project.budget), 0)).scalar() or 0
    total_spent = db.query(func.coalesce(func.sum(Invoice.amount), 0)).scalar() or 0

    projects = db.query(Project).all()
    project_count = len(projects)

    recent_documents = (
        db.query(Document)
        .order_by(Document.upload_date.desc())
        .limit(5)
        .all()
    )

    return {
        "summary": {
            "project_count": project_count,
            "total_budget": total_budget,
            "total_spent": total_spent,
            "remaining_budget": total_budget - total_spent,
        },
        "recent_documents": recent_documents,
    }


