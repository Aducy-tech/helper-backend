from typing import List
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class Cors(BaseSettings):
    model_config = {
        'env_file': '.env',
        'extra': 'ignore'
    }

    allowed_origins_str: str = Field(alias='ALLOWED_ORIGINS')
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

    @property
    def allowed_origins(self) -> List[str]:
        if ',' in self.allowed_origins_str:
            return self.allowed_origins_str.split(',')
        return [self.allowed_origins_str]


class DatabaseSettings(BaseSettings):
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_database: str

    echo: bool = False

    @property
    def url(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}'
            f'/{self.postgres_database}'
        )


class AuthJWT(BaseModel):
    keys_dir: Path = BASE_DIR / 'certs'

    private_key_path: Path = keys_dir / 'private.pem'
    public_key_path: Path = keys_dir / 'public.pem'

    access_token_name: str = 'access_token'
    refresh_token_name: str = 'refresh_token'

    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 43200  # 30 days

    algorithm: str = 'RS256'


class AI(BaseSettings):
    model_config = {
        'env_file': '.env',
        'extra': 'ignore'
    }

    proxy: str
    openai_api_key: str

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
