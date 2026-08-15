from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.ml_prediction import predict_risk, get_decision
from backend.database.connection import connection
router = APIRouter()

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
    Previous_Loan: str
    Education: str
    Home_Onwership: str
    Loan_Intent: str

@router.post("/predict")
def predict_loan(data: CustomerData):
    customer_data = {
        "Age": data.Age,
        "Gender": data.Gender,
        "Person Income": data.Person_Income,
        "Employee Experience": data.Employee_Experience,
        "Loan Amount": data.Loan_Amount,
        "Loan interest Rate": data.Loan_interest_Rate,
        "Loan percentage": data.Loan_percentage,
        "Credit History": data.Credit_History,
        "Credit Score": data.Credit_Score,
        "Previous Loan": data.Previous_Loan,
        "Education": data.Education,
        "Home Onwership": data.Home_Onwership,
        "Loan Intent": data.Loan_Intent
    }
    # ML prediction
    risk = predict_risk(customer_data)
    # Get current bank threshold from MySQL
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT safety_threshold
        FROM risk_settings
        WHERE id = 1""")
    setting = cursor.fetchone()
    cursor.close()
    threshold = float(setting["safety_threshold"])
    # Apply threshold
    result = get_decision(risk, threshold)
    return result

@router.post("/save")
def save_prediction(data: CustomerData):

    customer_data = {
        "Age": data.Age,
        "Gender": data.Gender,
        "Person Income": data.Person_Income,
        "Employee Experience": data.Employee_Experience,
        "Loan Amount": data.Loan_Amount,
        "Loan interest Rate": data.Loan_interest_Rate,
        "Loan percentage": data.Loan_percentage,
        "Credit History": data.Credit_History,
        "Credit Score": data.Credit_Score,
        "Previous Loan": data.Previous_Loan,
        "Education": data.Education,
        "Home Onwership": data.Home_Onwership,
        "Loan Intent": data.Loan_Intent
    }

    # ML prediction
    risk = predict_risk(customer_data)

    # Get current bank threshold
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT safety_threshold
        FROM risk_settings
        WHERE id = 1
    """)

    setting = cursor.fetchone()

    threshold = float(setting["safety_threshold"])

    # Apply threshold
    result = get_decision(risk, threshold)

    # Save prediction in MySQL
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
            previous_loan,
            education,
            home_ownership,
            loan_intent,
            risk_percentage,
            safety_percentage,
            threshold_used,
            decision
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        data.Previous_Loan,
        data.Education,
        data.Home_Onwership,
        data.Loan_Intent,
        float(result["risk_percentage"]),
        float(result["safety_percentage"]),
        int(threshold),
        result["decision"]
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()

    return {
        "message": "Prediction saved successfully",
        "risk_percentage": float(result["risk_percentage"]),
        "safety_percentage": float(result["safety_percentage"]),
        "threshold_used": int(threshold),
        "decision": result["decision"]
    }

@router.get("/predictions")
def get_predictions():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM loan_predictions
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    cursor.close()

    return predictions

@router.get("/predictions/approved")
def get_approved_predictions():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM loan_predictions
        WHERE decision = 'Approved'
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    cursor.close()

    return predictions


@router.get("/predictions/not-approved")
def get_not_approved_predictions():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM loan_predictions
        WHERE decision = 'Not Approved'
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    cursor.close()

    return predictions

@router.delete("/predictions/{prediction_id}")
def delete_prediction(prediction_id: int):

    cursor = connection.cursor()

    # Check if prediction exists
    cursor.execute(
        "SELECT id FROM loan_predictions WHERE id = %s",
        (prediction_id,)
    )

    existing = cursor.fetchone()

    if existing is None:
        cursor.close()
        return {"message": "Prediction not found"}

    # Delete prediction
    cursor.execute(
        "DELETE FROM loan_predictions WHERE id = %s",
        (prediction_id,)
    )

    connection.commit()

    cursor.close()

    return {
        "message": "Prediction deleted successfully",
        "id": prediction_id
    }