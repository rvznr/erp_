from fastapi import APIRouter

from app.api.routes import auth, dashboard, documents, finance, projects

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(projects.router)
api_router.include_router(documents.router)
api_router.include_router(finance.router)


