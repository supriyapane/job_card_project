import os

class Config:

    GEMINI_API_KEY = "AIzaSyD8K9Ojo0CoNW8hUXLaMnWKiUEMy_aWe6Q"
    DATABASE_URL = "sqlite:///database.db"
    SECRET_KEY = "mysecret7032547897"
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False