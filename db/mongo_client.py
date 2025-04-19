from pymongo import MongoClient

# Update this with your MongoDB URI (from MongoDB Atlas or local)
MONGO_URI = "mongodb://localhost:27017"  # Replace with Atlas URI if needed

client = MongoClient(MONGO_URI)
db = client["auth_app"]
users_collection = db["users"]
