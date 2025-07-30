# cython: embedsignature=True, annotation_typing=False
import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from . import include_sso
from .config import Settings

# .env をロード
load_dotenv(override=True)
settings = Settings()

app = FastAPI()
include_sso(app)

if __name__ == "__main__":
    kwargs = dict(host=settings.host, port=settings.port)
    if settings.reload:
        # リロード時は正しいモジュールパスを指定
        uvicorn.run(
            "moruapp_ms_sso.__main__:app",
            reload=True,
            **kwargs
        )
    else:
        uvicorn.run(
            app,
            reload=False,
            **kwargs
        )
