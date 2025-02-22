# src/app/config/settings.py

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")  # Read API key from .env
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")  # Read API key from .env

    class Config:
        env_file = ".env"
        # env_file_encoding = "utf-8"


# Create an instance of Settings to use throughout the app
settings = Settings()
