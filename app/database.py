from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

SQLALCHEMY_DATABASE_URL = f"postgresql://" \
                          f"{config('DATABASE_USERNAME', cast=str)}:" \
                          f"{config('DATABASE_PASSWORD', cast=str)}@" \
                          f"{config('DATABASE_HOSTNAME', cast=str)}:" \
                          f"{config('DATABASE_PORT', cast=str)}/" \
                          f"{config('DATABASE_NAME', cast=str)}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

print(engine.url)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi',
#             user='postgres',
#             password='Brian6894',
#             cursor_factory=RealDictCursor  # gives you the column names
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print(" Connecting to database failed")
#         print("Error", error)
#         time.sleep(2)
