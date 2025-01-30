from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client.telegram_bot
users_collection = db.users
chat_collection = db.chat_history
file_collection = db.file_metadata
