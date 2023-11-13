from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import env

dbHost = "" if env.DB_MYSQL_HOST == None else env.DB_MYSQL_HOST
dbPort = "" if env.DB_MYSQL_PORT == None else env.DB_MYSQL_PORT
dbName = "" if env.DB_MYSQL_NAME == None else env.DB_MYSQL_NAME
dbUser = "" if env.DB_MYSQL_USER == None else env.DB_MYSQL_USER
dbPass = "" if env.DB_MYSQL_PASS == None else env.DB_MYSQL_PASS

# Correctly construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"mysql://{dbUser}:{dbPass}@{dbHost}:{dbPort}/{dbName}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
