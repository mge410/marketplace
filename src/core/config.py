from enum import Enum
from pathlib import Path

from pydantic import PostgresDsn, BaseModel, AmqpDsn, EmailStr, AnyUrl, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Environment(Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class AppConfig(BaseModel):
    environment: Environment = Environment.DEV


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    workers: int | None = None


class ApiPrefix(BaseModel):
    api_prefix: str = "/api"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    token_type: str = "Bearer"
    access_token_expire_minutes: int = 30


class FastStreamConfig(BaseModel):
    url: AmqpDsn = AmqpDsn("amqp://guest:guest@rabbitmq:5672/")
    user_registered_event: str = "user-registered"


class S3Config(BaseModel):
    put_file_endpoint_url: AnyUrl = AnyUrl("http://localstack:4566")
    get_file_endpoint_url: AnyUrl = AnyUrl("http://localhost:4566")
    region_name: str = "eu-central-1"
    aws_access_key_id: str = "dev_s3_id"
    aws_secret_access_key: str = "dev_s3_key"
    bucket_name: str = "dev"


class EmailConfig(BaseModel):
    admin_email: EmailStr = "admin@marketplace.com"
    smtp_host: str = "maildev"
    smtp_port: int = 1025


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    app: AppConfig = AppConfig()
    email_config: EmailConfig = EmailConfig()
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    faststream: FastStreamConfig = FastStreamConfig()
    auth_jwt: AuthJWT = AuthJWT()
    s3_config: S3Config = S3Config()


settings = Settings.model_validate({})
