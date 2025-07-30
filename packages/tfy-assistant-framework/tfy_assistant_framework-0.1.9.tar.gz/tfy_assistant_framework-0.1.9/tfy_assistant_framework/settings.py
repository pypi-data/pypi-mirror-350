"""Settings for the Framework."""

import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv(dotenv_path=os.getenv("ENV_PATH", ".env"))


class Settings(BaseSettings):
    """Settings for the Framework."""

    local: bool = False
    openai_api_key: str
    openai_base_url: str
    openai_model_name: str

    # TrueFoundry settings
    tfy_base_url: str | None = None
    tfy_api_key: str | None = None
    tfy_assumed_user: str | None = None
    tfy_log_to_gateway: bool = True

    # NATS settings
    nats_url: str | None = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tfy_base_url = (
            self.tfy_base_url.rstrip("/") if self.tfy_base_url else self.tfy_base_url
        )

    @field_validator("nats_url")
    @classmethod
    def generate_tfy_nats_url(
        cls, value: str | None, info: ValidationInfo
    ) -> str | None:
        """Validate the NATS URL."""
        if value:
            return value

        tfy_base_url = info.data["tfy_base_url"]
        if tfy_base_url:
            parsed_url = urlparse(tfy_base_url)
            return f"wss://{parsed_url.hostname}/"

        # Return None as nats_url is not mandatory for all agents
        return None

    @property
    def tfy_host(self) -> str | None:
        if self.tfy_base_url:
            parsed_url = urlparse(self.tfy_base_url)
            return f"{parsed_url.scheme}://{parsed_url.netloc}"
        return None


settings = Settings()
