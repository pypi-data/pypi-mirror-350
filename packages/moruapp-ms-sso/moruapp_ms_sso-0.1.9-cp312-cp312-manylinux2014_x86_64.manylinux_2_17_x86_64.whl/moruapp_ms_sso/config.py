# cython: embedsignature=True, annotation_typing=False
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import Field

# .env を読み込む
load_dotenv(override=True)

class Settings(BaseSettings):
    # --- Azure AD SSO 設定 ---
    client_id: str = Field(..., env="CLIENT_ID")
    client_secret: str = Field(..., env="CLIENT_SECRET")
    tenant_id: str = Field(..., env="TENANT_ID")

    # --- フロントエンド コールバック URL ---
    frontend_redirect_uri: str = Field(..., env="FRONTEND_REDIRECT_URI")

    # --- サーバー起動設定 ---
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    reload: bool = Field(True, env="RELOAD")
    allow_insecure_http: bool = Field(False, env="ALLOW_INSECURE_HTTP")

    @property
    def backend_redirect_uri(self) -> str:
        return f"http://{self.host}:{self.port}/auth/callback"

    # --- JWT 設定 ---
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_cookie_name: str = Field("moru_sso_token", env="JWT_COOKIE_NAME")
    jwt_expire_seconds: int = Field(3600, env="JWT_EXPIRE_SECONDS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
