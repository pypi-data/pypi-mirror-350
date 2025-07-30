from pydantic import ConfigDict  # type: ignore
from pydantic_settings import BaseSettings  # type: ignore


class Settings(BaseSettings):
    """
    Settings for the AmbientAGI library with sensible defaults.
    These can be overridden by environment variables or user-defined settings.
    """

    MAIN_API_BASE_URL: str = (
        "http://insight-md-docker.eba-gen8ppse.eu-west-1.elasticbeanstalk.com"
    )
    SOLANA_API_BASE_URL: str = (
        "http://solana-toolkit-env.eba-mxurdvra.eu-west-1.elasticbeanstalk.com"
    )
    ETH_API_BASE_URL: str = (
        "http://etherum-env.eba-hm5jcqkt.eu-west-1.elasticbeanstalk.com"
    )
    FIRECRAWL_API_KEY: str = ""  # Placeholder key
    OPENAI_KEY: str = ""

    # Ensure defaults are used if environment variables are missing
    model_config = ConfigDict(env_prefix="AMBIENTAGI_", extra="allow")


# Ensure the settings object is initialized before use
settings = Settings()
