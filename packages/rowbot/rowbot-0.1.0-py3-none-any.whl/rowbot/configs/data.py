import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application's expected parameters.

    Pydantic's BaseSettings is leveraged to allow environment-based overrides
    without enforcing a prefix and treating them in a case-sensitive manner.
    """

    ROWBOT_DIR: str = os.path.expanduser("~/.rowbot")
    ROWBOT_FILE: str = os.path.join(ROWBOT_DIR, "commands.json")

    model_config = {
        "env_prefix": "",
        "case_sensitive": False,
    }


settings = Settings()
