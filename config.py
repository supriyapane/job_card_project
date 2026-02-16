
import os

class Config:

    GEMINI_API_KEY = "AIzaSyBNzEQmDCyBy95APxnSMmQDnFPxoVTEytM"
    DATABASE_URL = "sqlite:///database.db"
    SECRET_KEY = "mysecret7032547897"
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
