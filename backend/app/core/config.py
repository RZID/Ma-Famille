from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ma-famille-api"
    app_env: str = "development"
    api_v1_prefix: str = "/v1"
    backend_cors_origins: str = "http://localhost:5173,http://localhost:3000"
    database_url: str = "postgresql+psycopg://mafamille:mafamille@localhost:5432/mafamille"
    # Subpath hosting: "/ma-famille" in prod (college.rzidinc.com/ma-famille),
    # "" for local dev. FastAPI strips this prefix before routing and uses it
    # when generating /docs and /openapi.json URLs.
    root_path: str = ""
    doku_client_id: str = ""
    doku_secret_key: str = ""
    doku_base_url: str = "https://api-sandbox.doku.com"
    # Empty = open (local dev). Production sets this in backend/.env.
    manager_token: str = ""
    # Pending bookings older than this are auto-cancelled on next read/write.
    booking_ttl_minutes: int = 30

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.backend_cors_origins.split(",") if o.strip()]

    @property
    def doku_configured(self) -> bool:
        return bool(self.doku_client_id and self.doku_secret_key)


settings = Settings()
