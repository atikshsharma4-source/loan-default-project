from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.ml_prediction import predict_risk, get_decision
from backend.database.connection import connection


router = APIRouter()


# ==========================================
# Customer input model
# ==========================================

class CustomerData(BaseModel):

    Age: float
    Gender: str
    Person_Income: float
    Employee_Experience: float
    Loan_Amount: float
    Loan_interest_Rate: float
    Loan_percentage: float
    Credit_History: float
    Credit_Score: float
    Education: str
    Home_Onwership: str
    Loan_Intent: str


# ==========================================
# Convert API data to ML format
# ==========================================

def create_customer_data(data: CustomerData):

    return {
        "Age": data.Age,
        "Gender": data.Gender,
        "Person Income": data.Person_Income,
        "Employee Experience": data.Employee_Experience,
        "Loan Amount": data.Loan_Amount,
        "Loan interest Rate": data.Loan_interest_Rate,
        "Loan percentage": data.Loan_percentage,
        "Credit History": data.Credit_History,
        "Credit Score": data.Credit_Score,
        "Education": data.Education,
        "Home Onwership": data.Home_Onwership,
        "Loan Intent": data.Loan_Intent
    }


# ==========================================
# Get current bank safety threshold
# ==========================================

def get_current_threshold():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT safety_threshold
        FROM risk_settings
        WHERE id = 1
    """)

    setting = cursor.fetchone()

    cursor.close()

    if setting is None:
        return 90.0

    return float(setting["safety_threshold"])


# ==========================================
# PREDICT
# ==========================================

@router.post("/predict")
def predict_loan(data: CustomerData):

    customer_data = create_customer_data(data)

    # ML prediction
    risk = predict_risk(customer_data)

    # Get current bank threshold
    threshold = get_current_threshold()

    # Apply bank decision rule
    result = get_decision(
        risk,
        threshold
    )

    return result


# ==========================================
# SAVE PREDICTION
# ==========================================

@router.post("/save")
def save_prediction(data: CustomerData):

    customer_data = create_customer_data(data)

    # ML prediction
    risk = predict_risk(customer_data)

    # Get current bank threshold
    threshold = get_current_threshold()

    # Apply decision
    result = get_decision(
        risk,
        threshold
    )

    # ======================================
    # Save prediction in MySQL
    # ======================================

    cursor = connection.cursor()

    query = """
        INSERT INTO loan_predictions (
            age,
            gender,
            person_income,
            employee_experience,
            loan_amount,
            loan_interest_rate,
            loan_percentage,
            credit_history,
            credit_score,
            education,
            home_ownership,
            loan_intent,
            risk_percentage,
            safety_percentage,
            threshold_used,
            decision
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    values = (
        data.Age,
        data.Gender,
        data.Person_Income,
        data.Employee_Experience,
        data.Loan_Amount,
        data.Loan_interest_Rate,
        data.Loan_percentage,
        data.Credit_History,
        data.Credit_Score,
        data.Education,
        data.Home_Onwership,
        data.Loan_Intent,
        float(result["risk_percentage"]),
        float(result["safety_percentage"]),
        int(threshold),
        result["decision"]
    )

    cursor.execute(
        query,
        values
    )

    connection.commit()

    cursor.close()

    return {
        "message": "Prediction saved successfully",
        "risk_percentage": float(
            result["risk_percentage"]
        ),
        "safety_percentage": float(
            result["safety_percentage"]
        ),
        "threshold_used": int(threshold),
        "decision": result["decision"]
    }


# ==========================================
# GET ALL PREDICTIONS
# ==========================================

@router.get("/predictions")
def get_predictions():

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM loan_predictions
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    cursor.close()

    return predictions


# ==========================================
# GET APPROVED PREDICTIONS
# ==========================================

@router.get("/predictions/approved")
def get_approved_predictions():

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM loan_predictions
        WHERE decision = 'Approved'
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    cursor.close()

    return predictions


# ==========================================
# GET NOT-APPROVED PREDICTIONS
# ==========================================

@router.get("/predictions/not-approved")
def get_not_approved_predictions():

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM loan_predictions
        WHERE decision = 'Not Approved'
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    cursor.close()

    return predictions


# ==========================================
# DELETE PREDICTION
# ==========================================

@router.delete("/predictions/{prediction_id}")
def delete_prediction(
    prediction_id: int
):

    cursor = connection.cursor()

    # Check whether prediction exists
    cursor.execute(
        """
        SELECT id
        FROM loan_predictions
        WHERE id = %s
        """,
        (prediction_id,)
    )

    existing = cursor.fetchone()

    if existing is None:

        cursor.close()

        return {
            "message": "Prediction not found"
        }

    # Delete prediction
    cursor.execute(
        """
        DELETE FROM loan_predictions
        WHERE id = %s
        """,
        (prediction_id,)
    )

    connection.commit()

    cursor.close()

    return {
        "message": "Prediction deleted successfully",
        "id": prediction_id
    }