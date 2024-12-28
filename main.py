
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from backend.email_utils import send_verification_email, send_password_reset_email
from backend.models import User
from backend.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel

load_dotenv()
print("MAIL_PORT:", os.getenv("MAIL_PORT"))  # Debugging line to check MAIL_PORT
print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))  # Debugging line to check MAIL_USERNAME
print("MAIL_SERVER:", os.getenv("MAIL_SERVER"))  # Debugging line to check MAIL_SERVER

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5500",
    "http://localhost:3000",
    "https://myfrontendapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/welcome.html", response_class=HTMLResponse)  # New route for welcome.html
def read_welcome():
    with open("frontend/welcome.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/home.html", response_class=HTMLResponse)  # Route for home.html
def read_home():
    with open("frontend/home.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/settings.html", response_class=HTMLResponse)  # Route for settings.html
def read_settings():
    with open("frontend/settings.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/login.html", response_class=HTMLResponse)  # Route for login.html
def read_login():
    with open("frontend/login.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/blood_oxygen.html", response_class=HTMLResponse)  # Route for blood_oxygen.html
def read_blood_oxygen():
    with open("frontend/blood_oxygen.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/inhaler.html", response_class=HTMLResponse)  # Route for inhaler.html
def read_inhaler():
    with open("frontend/inhaler.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/heart.html", response_class=HTMLResponse)  # Route for heart.html
def read_heart():
    with open("frontend/heart.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/respiratory.html", response_class=HTMLResponse)  # Route for respiratory.html
def read_respiratory():
    with open("frontend/respiratory.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@app.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(username=user.username, email=user.email, password=user.password)  # Ensure password is hashed in production
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.get("/update-sensor-data")
async def update_sensor_data(value: float):
    # Here you can store the sensor data in a database or process it as needed
    # Here you can store the sensor data in a database or process it as needed
    # For demonstration, let's assume we are returning static values
    heart_rate = 75  # Example static value
    blood_oxygen = 98  # Example static value
    print(f"Received sensor data: {value}")
    return {"heart_rate": heart_rate, "blood_oxygen": blood_oxygen}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
