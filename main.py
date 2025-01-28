# main.py
from fastapi import FastAPI,HTTPException
from auth import login_func,register_user
from dash import fetch_users,total_users,new_users
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import date,datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId 
import os
# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials from environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")


# Create a global MongoDB client (prevents multiple connections)
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
users_collection = db[MONGO_COLLECTION]

# Create an instance of FastAPI
app = FastAPI()

# Pydantic model for login request
class LoginRequest(BaseModel):
    username: str
    password: str
class RegisterRequest(BaseModel):
    username: str
    email: str
    password:str

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Define a root endpoint
@app.post("/login")
def login(request: LoginRequest):
    print(request)
    username = request.username
    password = request.password
    return login_func(username,password)

@app.get("/users")
def get_users():
    return fetch_users()

@app.get("/users/total")
def get_total_users():
    return total_users()

@app.get("/users/new")
def get_new_users():
    return new_users()

@app.post("/register")
def register(request:RegisterRequest):
    username = request.username
    password = request.password
    email = request.email
    role = "user"
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    return register_user(username,email,password,today,role)

# Define another endpoint
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        # Convert user_id from string to ObjectId
        user_object_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Delete the user from the database
    result = users_collection.delete_one({"_id": user_object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}