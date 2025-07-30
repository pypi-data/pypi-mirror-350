from pydantic import BaseModel


class AuthConfig(BaseModel):
    username: str
    client_id: str
    base_url: str
    token: str
