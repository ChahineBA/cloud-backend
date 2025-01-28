from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
from datetime import datetime

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

def fetch_users():
    # Retrieve all documents
    documents = users_collection.find()

    # Convert ObjectId to string and return the list of documents
    documents_list = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        documents_list.append(doc)
    
    return documents_list

def total_users():
    users = fetch_users()
    total = len(users)
    return total

def new_users():
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    # Query for documents with today's date
    results = users_collection.count_documents({"date": today})
    return results