from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class ProjectBase(SQLModel):
    name: str
    client_name: Optional[str] = None
    status: str = Field(default="Planned", index=True)  # Planned, In Progress, Completed
    budget: float = 0
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    documents: list["Document"] = Relationship(back_populates="project")
    invoices: list["Invoice"] = Relationship(back_populates="project")


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime


