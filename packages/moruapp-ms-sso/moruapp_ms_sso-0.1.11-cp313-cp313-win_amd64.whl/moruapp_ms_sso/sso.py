# cython: embedsignature=True, annotation_typing=False
# ----- moruapp_ms_sso/sso.py -----
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from urllib.parse import quote

from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_sso.sso.microsoft import MicrosoftSSO
import jwt

from .config import Settings

router = APIRouter(prefix="/auth", tags=["sso"])
settings = Settings()

host_for_callback = "localhost" if settings.host in ("0.0.0.0", "::0") else settings.host
backend_callback = f"http://{host_for_callback}:{settings.port}/auth/callback"

_sso = MicrosoftSSO(
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    tenant=settings.tenant_id,
    redirect_uri=backend_callback,
    allow_insecure_http=settings.allow_insecure_http,
)

@router.get("/login")
async def login():
    async with _sso:
        return await _sso.get_login_redirect()

@router.get("/callback")
async def callback(request: Request):
    async with _sso:
        user = await _sso.verify_and_process(request)

    # dict 化
    if hasattr(user, "dict"):
        user_data = user.dict()
    elif isinstance(user, dict):
        user_data = user
    else:
        user_data = user.__dict__

    # JWT 作成
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_expire_seconds)
    payload = {**user_data, "exp": expire}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    secure_flag = not settings.allow_insecure_http
    samesite_flag = "lax" if settings.allow_insecure_http else "none"
    response = RedirectResponse(url=settings.frontend_redirect_uri, status_code=302)
    response.set_cookie(
        key=settings.jwt_cookie_name,
        value=token,
        httponly=True,
        secure=secure_flag,
        samesite=samesite_flag,
        path="/",
        max_age=settings.jwt_expire_seconds,
    )
    return response

security = HTTPBearer(auto_error=False)

def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Optional[Dict[str, Any]]:
    token = credentials.credentials if credentials else request.cookies.get(settings.jwt_cookie_name)
    if not token:
        return None
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None

@router.post("/logout")
async def logout(response: Response):
    """
    ログアウト：JWT クッキーを削除して、クライアントに通知します。
    フロント側ではこのエンドポイントを呼び出した後、
    必要に応じてログイン画面などにリダイレクトしてください。
    """
    secure_flag = not settings.allow_insecure_http
    samesite_flag = "lax" if settings.allow_insecure_http else "none"

    # クッキーを削除
    response.delete_cookie(
        key=settings.jwt_cookie_name,
        path="/",
        httponly=True,
        secure=secure_flag,
        samesite=samesite_flag,
    )
    return JSONResponse({"detail": "Logged out"})

@router.get("/user")
async def user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return current_user

def include_sso(app):
    # CORS はアプリ側で設定する想定
    app.include_router(router)
