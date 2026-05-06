import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This gets the database link from Docker or GitHub Actions.
# If there is no database link, it uses a simple local SQLite database.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./calculator_app.db")

# SQLite needs this extra setting.
# PostgreSQL does not need it.
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# This connects SQLAlchemy to the database.
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# This creates database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class our models will use.
Base = declarative_base()


# This function gives the app access to the database.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()