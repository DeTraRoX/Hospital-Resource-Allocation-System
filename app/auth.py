from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, Session, select
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import jwt
from ..db import get_session

# Secret key for JWT
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/auth", tags=["Auth"])

# ✅ User model
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

# --- Token helper ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)

# --- Routes ---
@router.post("/register")
def register(username: str, password: str, session: Session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.username == username)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = bcrypt.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"msg": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Get current user ---
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
