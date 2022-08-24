import random
import string

from passlib.hash import bcrypt

from app.config import JWT_SECRET
from decouple import config
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app
from app.database import Base


def random_email(k):
    return ''.join(random.choice(string.ascii_lowercase)
                   for _ in range(k)) + "@gmail.com"


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


def get_test_user_token() -> str:
    user_data = {
        "id": '1',
        "username": 'test_user',
        "password_hash": bcrypt.hash('password')
    }
    token = jwt.encode(user_data, JWT_SECRET)
    return token


SQLALCHEMY_DATABASE_URL = f"postgresql://" \
                          f"{config('DATABASE_USERNAME', cast=str)}:" \
                          f"{config('DATABASE_PASSWORD', cast=str)}@" \
                          f"{config('DATABASE_HOSTNAME', cast=str)}:" \
                          f"{config('DATABASE_PORT', cast=str)}/" \
                          f"{config('DATABASE_NAME', cast=str)}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
