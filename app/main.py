from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.models.calculation import Calculation
from app.routes.calculations import router as calculation_router


# This creates the database tables when the app starts.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="IS601 Final Project Calculator App",
    description="A FastAPI app that saves calculation history and shows reports.",
    version="1.0.0",
)


app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(calculation_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the IS601 Calculator History App",
        "docs": "Go to /docs to test the API",
    }