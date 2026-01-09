import os
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.deps import get_current_active_user, get_db
from app.models.document import Document, DocumentCreate, DocumentRead
from app.models.project import Project
from app.models.user import User

router = APIRouter(prefix="/documents", tags=["documents"])

settings = get_settings()


@router.post(
    "/upload",
    response_model=DocumentRead,
)
async def upload_document(
    project_id: int = Form(...),
    category: str = Form(...),
    notes: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    os.makedirs(settings.FILE_STORAGE_PATH, exist_ok=True)
    file_location = os.path.join(settings.FILE_STORAGE_PATH, file.filename)

    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    doc = Document(
        project_id=project_id,
        category=category,
        notes=notes,
        file_name=file.filename,
        file_path=file_location,
        uploader_id=current_user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/", response_model=List[DocumentRead])
def list_documents(project_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Document)
    if project_id is not None:
        query = query.filter(Document.project_id == project_id)
    return query.order_by(Document.upload_date.desc()).all()


