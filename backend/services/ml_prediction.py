import pickle
import pandas as pd


# ==============================
# Load trained ML pipeline
# ==============================

with open("ml/loan_default_pipeline.pkl", "rb") as file:
    model_pipeline = pickle.load(file)

print("ML pipeline loaded successfully!")


# ==============================
# Load ML threshold
# ==============================

with open("ml/loan_default_threshold.pkl", "rb") as file:
    model_threshold = pickle.load(file)

print(f"ML threshold loaded successfully: {model_threshold}")


# ==============================
# Prepare customer features
# ==============================

def prepare_features(data):

    df = pd.DataFrame([data])

    # Normalize categorical values
    df["Gender"] = (
        df["Gender"].astype(str).str.strip().str.lower()
    )

    df["Education"] = (
        df["Education"].astype(str).str.strip().str.lower()
    )

    df["Home Onwership"] = (
        df["Home Onwership"].astype(str).str.strip().str.lower()
    )

    df["Loan Intent"] = (
        df["Loan Intent"].astype(str).str.strip().str.lower()
    )

    # Feature engineering
    df["Income_per_Experience"] = (
        df["Person Income"] /
        (df["Employee Experience"] + 1)
    )

    df["Loan_Income_Ratio"] = (
        df["Loan Amount"] /
        df["Person Income"]
    )

    df["Interest_Burden"] = (
        df["Loan Amount"] *
        df["Loan interest Rate"]
    )

    # Exact features used during training
    feature_columns = [
        "Age",
        "Gender",
        "Education",
        "Person Income",
        "Employee Experience",
        "Home Onwership",
        "Loan Amount",
        "Loan Intent",
        "Loan interest Rate",
        "Loan percentage",
        "Credit History",
        "Credit Score",
        "Income_per_Experience",
        "Loan_Income_Ratio",
        "Interest_Burden"
    ]

    df = df[feature_columns]

    return df


# ==============================
# Predict default risk
# ==============================

def predict_risk(data):

    features = prepare_features(data)

    probabilities = model_pipeline.predict_proba(features)

    default_probability = probabilities[0][1]

    risk_percentage = default_probability * 100

    return float(risk_percentage)


# ==============================
# Bank decision
# ==============================

def get_decision(risk_percentage, safety_threshold):

    safety_percentage = 100 - risk_percentage

    if safety_percentage >= safety_threshold:
        decision = "Approved"
    else:
        decision = "Not Approved"

    return {
        "risk_percentage": float(risk_percentage),
        "safety_percentage": float(safety_percentage),
        "threshold_used": float(safety_threshold),
        "decision": decision
    }