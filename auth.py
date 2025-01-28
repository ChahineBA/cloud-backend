from pymongo import MongoClient
import bcrypt
from dotenv import load_dotenv
from bson import ObjectId
import os


# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials from environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")


# Create a global MongoDB client (prevents multiple connections)
client = MongoClient(MONGO_URI,tlsAllowInvalidCertificates=True)
db = client[MONGO_DB]
users_collection = db[MONGO_COLLECTION]

# Find user and verify password
def find_user(username, password, user_collection):
    """Finds a user by username and verifies the password."""
    user = user_collection.find_one({"username": username})
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return user  # Authentication successful
    return None  # Invalid username or password

# Register a new user
def register_user(username, email, password,date,role):
    """Registers a new user with a hashed password and returns a message with a color code."""
    try:
        # Check if username or email already exists
        if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
            return "Username or email already exists.", "red"

        # Hash the password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user into the database
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "date":date,
            "role":role  # Store hashed password as bytes
        }
        users_collection.insert_one(user_data)
        return "User registered successfully!", "green"

    except Exception as e:
        return f"Error registering user: {e}", "red"

# Login function
def login_func(username, password):
    """Handles user login and returns a message with a color code."""  
    # Get the user collection
    user = find_user(username, password, users_collection)

    if user:
        return "Login successful!", "green",user["role"]
    else:
        return "Invalid username or password!", "red",user["role"]

def fetch_users():
    # Retrieve all documents
    documents = users_collection.find()

    # Convert ObjectId to string and return the list of documents
    documents_list = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        documents_list.append(doc)
    
    return documents_list