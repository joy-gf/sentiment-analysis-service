"""
Configuration settings for the sentiment analysis service
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # ML Model
    MODEL_NAME: str = os.getenv("MODEL_NAME", "pysentimiento/robertuito-sentiment-analysis")
    DEVICE: str = os.getenv("DEVICE", "cpu")  # Use "cuda" if GPU available

    # CORS
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5000,http://localhost:3000"
    ).split(",")


settings = Settings()
