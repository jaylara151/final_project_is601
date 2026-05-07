from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.calculation import (
    CalculationCreate,
    CalculationUpdate,
    CalculationResponse,
    CalculationReport,
)
from app.services.calculation_service import (
    create_calculation,
    get_all_calculations,
    get_one_calculation,
    update_calculation_note,
    delete_calculation,
    get_calculation_report,
)


router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


@router.post("/", response_model=CalculationResponse)
def add_calculation(calculation: CalculationCreate, db: Session = Depends(get_db)):
    try:
        new_calculation = create_calculation(db, calculation)
        return new_calculation

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=List[CalculationResponse])
def read_all_calculations(db: Session = Depends(get_db)):
    calculations = get_all_calculations(db)
    return calculations


@router.get("/report/summary", response_model=CalculationReport)
def read_calculation_report(db: Session = Depends(get_db)):
    report = get_calculation_report(db)
    return report


@router.get("/{calculation_id}", response_model=CalculationResponse)
def read_one_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calculation = get_one_calculation(db, calculation_id)

    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation was not found.")

    return calculation


@router.put("/{calculation_id}", response_model=CalculationResponse)
def edit_calculation_note(
    calculation_id: int,
    calculation_update: CalculationUpdate,
    db: Session = Depends(get_db),
):
    calculation = update_calculation_note(
        db,
        calculation_id,
        calculation_update.note,
    )

    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation was not found.")

    return calculation


@router.delete("/{calculation_id}")
def remove_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calculation = delete_calculation(db, calculation_id)

    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation was not found.")

    return {"message": "Calculation deleted successfully."}