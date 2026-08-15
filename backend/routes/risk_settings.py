from fastapi import APIRouter
from backend.database.connection import connection

router = APIRouter()


@router.get("/risk-threshold")
def get_risk_threshold():

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT safety_threshold
        FROM risk_settings
        WHERE id = 1
    """

    cursor.execute(query)

    setting = cursor.fetchone()

    cursor.close()

    return {
        "safety_threshold": setting["safety_threshold"]
    }

@router.put("/risk-threshold")
def update_risk_threshold(safety_threshold: float):
    if safety_threshold < 0 or safety_threshold > 100:
        return {
            "message": "Threshold must be between 0 and 100"
        }
    cursor = connection.cursor()
    query = """
        UPDATE risk_settings
        SET safety_threshold = %s
        WHERE id = 1"""
    cursor.execute(query, (safety_threshold,))
    connection.commit()
    cursor.close()
    return {
        "message": "Risk threshold updated successfully",
        "new_threshold": safety_threshold}