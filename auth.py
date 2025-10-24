from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .models import User, UserCreate, UserLogin  # Import UserLogin
from .database import get_db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  # Catch broader DB errors
import logging  # For logging errors

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login", response_model=dict)
async def login(user: UserLogin, db: Session = Depends(get_db)):  # Changed to UserLogin (no email required)
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"message": "Login successful", "username": user.username}

@router.post("/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check for existing username or email
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration failed due to duplicate data or constraint violation")
    except SQLAlchemyError as e:  # Catch broader DB errors
        db.rollback()
        logger.error(f"Database error during registration: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:  # Catch any other unexpected errors
        db.rollback()
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return {"message": "User registered successfully", "username": user.username}