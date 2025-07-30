from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Agent, Admin
from datetime import datetime
from schemas import RegisterAgentRequest, LoginRequest, TokenResponse, AgentLoginRequest, AgentInfo
from auth import hash_secret, verify_secret, create_token, decode_token

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Agent Auth Service")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

def get_current_admin(Authorization: str = Header(...)):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    payload = decode_token(Authorization.split(" ")[1])
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return payload

@app.post("/admin/init", status_code=201)
def create_admin(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(Admin).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="Admin already exists")
    db.add(Admin(username=username, hashed_password=hash_secret(password)))
    db.commit()
    return {"msg": "Admin created"}

@app.post("/admin/login", response_model=TokenResponse)
def admin_login(request: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(username=request.username).first()
    if not admin or not verify_secret(request.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    token, expire = create_token({"sub": admin.username, "role": "admin"})
    return {"access_token": token, "expires_in": int((expire - datetime.utcnow()).total_seconds())}

@app.post("/agents/register", status_code=201)
def register_agent(request: RegisterAgentRequest, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    if db.query(Agent).filter_by(agent_id=request.agent_id).first():
        raise HTTPException(status_code=400, detail="Agent already exists")
    db.add(Agent(agent_id=request.agent_id, hashed_secret=hash_secret(request.agent_secret)))
    db.commit()
    return {"msg": "Agent registered"}

@app.post("/token", response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    agent = db.query(Agent).filter_by(agent_id=form_data.username).first()
    if not agent or not verify_secret(form_data.password, agent.hashed_secret):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token, expire = create_token({"sub": agent.agent_id, "role": "agent"})
    return {"access_token": token, "token_type": "bearer", "expires_in": int((expire - datetime.utcnow()).total_seconds())}

@app.get("/me")
def read_users_me(user=Depends(get_current_user)):
    return {"id": user["sub"], "role": user["role"]}

@app.get("/admin/agents", response_model=list[AgentInfo])
def list_agents(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    agents = db.query(Agent).all()
    return [{"agent_id": a.agent_id} for a in agents]
