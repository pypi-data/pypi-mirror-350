from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # GitHub
    URL_GITHUB_TEMPLATE: str = 'https://raw.githubusercontent.com/github/gitignore/master/{stack}.gitignore'

    # Settings for Pydantic Settings
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


settings = Settings()
