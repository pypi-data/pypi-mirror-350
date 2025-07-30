from pydantic import BaseModel

class RegisterAgentRequest(BaseModel):
    agent_id: str
    agent_secret: str

class LoginRequest(BaseModel):
    username: str
    password: str

class AgentLoginRequest(BaseModel):
    agent_id: str
    agent_secret: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class AgentInfo(BaseModel):
    agent_id: str
