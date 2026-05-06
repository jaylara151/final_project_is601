from collections import Counter
from sqlalchemy.orm import Session

from app.models.calculation import Calculation


def calculate_result(first_number: float, second_number: float, operation: str):
    operation = operation.lower()

    if operation == "add":
        return first_number + second_number

    if operation == "subtract":
        return first_number - second_number

    if operation == "multiply":
        return first_number * second_number

    if operation == "divide":
        if second_number == 0:
            raise ValueError("You cannot divide by zero.")
        return first_number / second_number

    raise ValueError("Invalid operation. Use add, subtract, multiply, or divide.")


def create_calculation(db: Session, calculation_data):
    result = calculate_result(
        calculation_data.first_number,
        calculation_data.second_number,
        calculation_data.operation,
    )

    new_calculation = Calculation(
        first_number=calculation_data.first_number,
        second_number=calculation_data.second_number,
        operation=calculation_data.operation.lower(),
        result=result,
        note=calculation_data.note,
    )

    db.add(new_calculation)
    db.commit()
    db.refresh(new_calculation)

    return new_calculation


def get_all_calculations(db: Session):
    return db.query(Calculation).order_by(Calculation.id.desc()).all()


def get_one_calculation(db: Session, calculation_id: int):
    return db.query(Calculation).filter(Calculation.id == calculation_id).first()


def update_calculation_note(db: Session, calculation_id: int, note: str):
    calculation = get_one_calculation(db, calculation_id)

    if calculation is None:
        return None

    calculation.note = note

    db.commit()
    db.refresh(calculation)

    return calculation


def delete_calculation(db: Session, calculation_id: int):
    calculation = get_one_calculation(db, calculation_id)

    if calculation is None:
        return None

    db.delete(calculation)
    db.commit()

    return calculation


def get_calculation_report(db: Session):
    calculations = db.query(Calculation).all()

    if len(calculations) == 0:
        return {
            "total_calculations": 0,
            "average_result": None,
            "highest_result": None,
            "lowest_result": None,
            "most_common_operation": None,
            "latest_result": None,
        }

    results = [calculation.result for calculation in calculations]
    operations = [calculation.operation for calculation in calculations]

    most_common_operation = Counter(operations).most_common(1)[0][0]
    latest_calculation = max(calculations, key=lambda calculation: calculation.created_at)

    return {
        "total_calculations": len(calculations),
        "average_result": sum(results) / len(results),
        "highest_result": max(results),
        "lowest_result": min(results),
        "most_common_operation": most_common_operation,
        "latest_result": latest_calculation.result,
    }