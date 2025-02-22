import os
from typing import List
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent


class Cors(BaseModel):
    allowed_origins: List[str] = os.getenv(
        "ALLOWED_ORIGINS",
        ""
    ).split(",")
    allow_credentials: bool = True
    allowed_methods: List[str] = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "OPTIONS"
    ]
    allowed_headers: List[str] = [
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With"
    ]


class DatabaseSettings(BaseModel):
    db_user: str = os.getenv("POSTGRES_USER")
    db_password: str = os.getenv("POSTGRES_PASSWORD")
    db_host: str = os.getenv("POSTGRES_HOST")
    db_name: str = os.getenv("POSTGRES_DATABASE")
    db_port: str = os.getenv("POSTGRES_PORT", "5432")

    url: str = (
        f'postgresql+asyncpg://{db_user}:{db_password}'
        f'@{db_host}:{db_port}/{db_name}'
    )

    echo: bool = False


class AuthJWT(BaseModel):
    keys_dir: Path = BASE_DIR / 'certs'

    private_key_path: Path = keys_dir / 'private.pem'
    public_key_path: Path = keys_dir / 'public.pem'

    access_token_name: str = 'access_token'
    refresh_token_name: str = 'refresh_token'

    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 43200  # 30 days

    algorithm: str = 'RS256'


class AI(BaseModel):
    proxy: str = os.getenv('PROXY')
    openai_api_key: str = os.getenv('OPENAI_API_KEY')

    system_text_for_essay: str = """
    Ни в коем случае не используй слова, кроме русских.

    Генерация сочинений: пиши так, будто ты человек, который пишет сочинение.
    """

    min_tokens_for_essay: int = 750
    min_tokens_for_ai: int = 500


class Settings(BaseModel):
    auth_jwt: AuthJWT = AuthJWT()
    database_settings: DatabaseSettings = DatabaseSettings()
    ai: AI = AI()
    cors: Cors = Cors()


settings = Settings()
