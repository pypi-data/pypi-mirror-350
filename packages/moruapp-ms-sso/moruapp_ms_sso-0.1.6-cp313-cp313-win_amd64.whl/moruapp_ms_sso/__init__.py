# cython: embedsignature=True, annotation_typing=False
# ----- moruapp_ms_sso/__init__.py -----
from fastapi import FastAPI
from .sso import router as sso_router
from .config import Settings

__version__ = "0.1.6"
__all__ = ["include_sso", "Settings", "sso_router"]

def include_sso(app: FastAPI):
    app.include_router(sso_router)