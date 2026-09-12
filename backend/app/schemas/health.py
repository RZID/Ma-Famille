from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "ma-famille-api"


class DbHealthResponse(BaseModel):
    status: str = "ok"
    database: str = "reachable"


class RootResponse(BaseModel):
    service: str = "ma-famille-api"
    env: str = "development"
