from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models.calculation import Calculation
from app.routes.calculations import router as calculation_router
from app.schemas.calculation import CalculationCreate
from app.services.calculation_service import (
    create_calculation,
    get_all_calculations,
    get_one_calculation,
    update_calculation_note,
    delete_calculation,
    get_calculation_report,
)


# This creates the database tables when the app starts.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="IS601 Final Project Calculator App",
    description="A FastAPI app that saves calculation history and shows reports.",
    version="1.0.0",
)


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


# API routes for Swagger
app.include_router(calculation_router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None,
        },
    )


@app.post("/calculate")
def calculate_from_form(
    request: Request,
    first_number: float = Form(...),
    second_number: float = Form(...),
    operation: str = Form(...),
    note: str = Form(""),
    db: Session = Depends(get_db),
):
    calculation_data = CalculationCreate(
        first_number=first_number,
        second_number=second_number,
        operation=operation,
        note=note,
    )

    try:
        create_calculation(db, calculation_data)
        return RedirectResponse(url="/history", status_code=303)

    except ValueError as error:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(error),
            },
        )


@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request, db: Session = Depends(get_db)):
    calculations = get_all_calculations(db)

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "calculations": calculations,
        },
    )


@app.get("/history/{calculation_id}", response_class=HTMLResponse)
def detail_page(
    calculation_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    calculation = get_one_calculation(db, calculation_id)

    return templates.TemplateResponse(
        request=request,
        name="detail.html",
        context={
            "calculation": calculation,
        },
    )


@app.post("/history/{calculation_id}/edit")
def edit_note_from_form(
    calculation_id: int,
    note: str = Form(...),
    db: Session = Depends(get_db),
):
    update_calculation_note(db, calculation_id, note)

    return RedirectResponse(url="/history", status_code=303)


@app.post("/history/{calculation_id}/delete")
def delete_from_form(
    calculation_id: int,
    db: Session = Depends(get_db),
):
    delete_calculation(db, calculation_id)

    return RedirectResponse(url="/history", status_code=303)


@app.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request, db: Session = Depends(get_db)):
    report = get_calculation_report(db)

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "report": report,
        },
    )