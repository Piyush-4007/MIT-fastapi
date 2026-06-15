# app.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

# ==========================================
# 1. DATABASE SETUP (SQLAlchemy)
# ==========================================
# 'check_same_thread': False is required for SQLite when used with FastAPI
engine = create_engine("sqlite:///fastapi_users.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)

# Create the tables
Base.metadata.create_all(bind=engine)

# ==========================================
# 2. DATA VALIDATION (Pydantic)
# ==========================================
# Schema for creating a user (User sends this)
class UserCreate(BaseModel):
    name: str
    email: str

# Schema for reading a user (API returns this)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy objects

# ==========================================
# 3. FASTAPI APPLICATION
# ==========================================
app = FastAPI()

# Dependency: Opens a database session for each request and closes it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CREATE ---
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    stmt = select(User).where(User.email == user.email)
    existing_user = db.scalars(stmt).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create and save new user
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Retrieves the newly generated ID
    return db_user

# --- READ ALL ---
@app.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()
    return users

# --- UPDATE ---
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = updated_user.name
    db_user.email = updated_user.email
    db.commit()
    db.refresh(db_user)
    return db_user

# --- DELETE ---
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}