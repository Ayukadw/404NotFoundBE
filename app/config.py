import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "superjwtsecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
