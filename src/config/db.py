from fastapi import FastAPI
from pymongo import AsyncMongoClient
from .env import MONGO_URL, DB_NAME


client = AsyncMongoClient(MONGO_URL)

dbClient = client[DB_NAME]

async def connect_to_db():
    print("Connecting  to MongoDB!")

    await client.aconnect()

    print("Connected to MongoDB!")

async def close_db():
    await client.aclose()
    print("MongoDB connection closed.")