from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_CONFIG = {
    "host": os.getenv("MONGO_HOST", "localhost"),
    "port": int(os.getenv("MONGO_PORT", "27017")),
    "db": os.getenv("MONGO_DB"),
    "username": os.getenv("MONGO_USER"),
    "password": os.getenv("MONGO_PASSWORD")
}

def get_mongo_client():
    config = MONGO_CONFIG
    uri = f"mongodb://{config['username']}:{config['password']}@{config['host']}:{config['port']}"
    return MongoClient(uri)[config["db"]]
