from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.project import Project
from app.models.user import User


def init() -> None:
    db: Session = SessionLocal()
    try:
        create_admin(db)
        create_sample_data(db)
    finally:
        db.close()


def create_admin(db: Session) -> None:
    admin_email = "admin@kucuklerinsaat.com"
    admin = db.query(User).filter(User.email == admin_email).first()
    if admin:
        return
    admin = User(
        email=admin_email,
        full_name="ERP Admin",
        role="Admin",
        hashed_password=get_password_hash("Admin123!"),
    )
    db.add(admin)
    db.commit()


def create_sample_data(db: Session) -> None:
    if db.query(Project).count() > 0:
        return
    demo_project = Project(
        name="Merkez Ofis Yenileme",
        client_name="Küçükler İnşaat",
        status="In Progress",
        budget=500000,
    )
    db.add(demo_project)
    db.commit()


