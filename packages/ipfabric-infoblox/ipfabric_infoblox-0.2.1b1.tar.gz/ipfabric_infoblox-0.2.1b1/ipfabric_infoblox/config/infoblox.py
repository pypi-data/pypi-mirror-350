from typing import Optional, Union
import ssl
from httpx import URL
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from .models import TimeoutTypes


class Infoblox(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="ib_", extra="ignore")
    host: Union[str, URL] = Field(None)
    verify: Union[ssl.SSLContext, bool, str] = True
    timeout: Union[TimeoutTypes] = 5.0
    username: str
    password: str
    import_timeout: int = 60
    import_retry: int = 10
    discovery_timeout: int = 60
    discovery_retry: int = 10

