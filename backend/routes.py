from sqlalchemy.orm import Session
from .database import get_db
from .models import User, MedicationUsage
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .email_utils import send_verification_email, send_password_reset_email
from .utils import verify_password, hash_password

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class MedicationUsageCreate(BaseModel):
    user_id: int
    medication_name: str
    dosage: float
    date_taken: str

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    send_verification_email(user.email)
    return db_user

@router.post("/password-reset/")
def password_reset(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    send_password_reset_email(user.email)
    return {"message": "Password reset email sent"}

@router.post("/verify-email/")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid token")
    user.is_active = True
    user.verification_token = None 
    db.commit()
    return {"message": "Email has been verified successfully"}

@router.post("/reset-password/")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid token")
    user.password = hash_password(new_password)
    user.verification_token = None
    db.commit()
    return {"message": "Password has been reset successfully"}

@router.get("/users/{user_id}")
def get_user_data(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return {"user_id": user.id, "username": user.username, "email": user.email}

@router.post("/medication/")
def log_medication_usage(medication: MedicationUsageCreate, db: Session = Depends(get_db)):
    medication_entry = MedicationUsage(user_id=medication.user_id, medication_name=medication.medication_name, dosage=medication.dosage, date_taken=medication.date_taken)
    db.add(medication_entry)
    db.commit()
    return {"message": "Medication logged successfully"}
