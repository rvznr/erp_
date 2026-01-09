from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class DocumentBase(SQLModel):
    category: str = Field(index=True)  # Contracts, Invoices, Site Photos, Permits
    file_name: str
    file_path: str
    notes: Optional[str] = None


class Document(DocumentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    uploader_id: int = Field(foreign_key="user.id", index=True)
    upload_date: datetime = Field(default_factory=datetime.utcnow)

    project: Optional["Project"] = Relationship(back_populates="documents")


class DocumentCreate(SQLModel):
    project_id: int
    category: str
    notes: Optional[str] = None


class DocumentRead(DocumentBase):
    id: int
    project_id: int
    uploader_id: int
    upload_date: datetime


