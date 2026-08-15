import pickle
import pandas as pd
with open("ml/loan_default_xgboost.pkl", "rb") as file:
    model = pickle.load(file)

with open("ml/scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

with open("ml/feature_names.pkl", "rb") as file:
    feature_names = pickle.load(file)

print("ML model loaded successfully!")
print("Scaler loaded successfully!")
print("Feature names loaded successfully!")

print("\nFeature names expected by model:")
for i, feature in enumerate(feature_names):
    print(i, feature)

def prepare_features(data):
    df = pd.DataFrame([data])

    # Calculate features exactly as used during training
    df["Income_per_Experience"] = (
        df["Person Income"] / (df["Employee Experience"] + 1)
    )

    df["Interest_Burden"] = (
        df["Loan Amount"] * df["Loan interest Rate"]
    )

    # Convert Gender
    df["Gender"] = df["Gender"].map({
        "Male": 1,
        "Female": 0
    })

    # Convert Previous Loan
    df["Previous Loan"] = df["Previous Loan"].map({
        "Yes": 1,
        "No": 0
    })

    # One-hot encode categorical columns
    df = pd.get_dummies(
        df,
        columns=["Education", "Home Onwership", "Loan Intent"],
        drop_first=True
    )

    # Add missing model columns with 0
    for feature in feature_names:
        if feature not in df.columns:
            df[feature] = 0

    # Keep exact 24-feature order
    df = df[feature_names]

    # These are the 10 columns scaled during training
    continuous_cols = [
        "Age",
        "Person Income",
        "Employee Experience",
        "Loan Amount",
        "Loan interest Rate",
        "Loan percentage",
        "Credit History",
        "Credit Score",
        "Income_per_Experience",
        "Interest_Burden"
    ]

    # Use the already-trained scaler
    df[continuous_cols] = scaler.transform(df[continuous_cols])

    return df

def predict_risk(data):
    # Prepare the customer's features
    features = prepare_features(data)

    # Get probability from XGBoost
    probabilities = model.predict_proba(features)

    # Probability of default (class 1)
    default_probability = probabilities[0][1]

    # Convert to percentage
    risk_percentage = default_probability * 100

    return risk_percentage

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

    

test_data = {
    "Age": 30,
    "Gender": "Male",
    "Person Income": 500000,
    "Employee Experience": 5,
    "Loan Amount": 200000,
    "Loan interest Rate": 10,
    "Loan percentage": 40,
    "Credit History": 5,
    "Credit Score": 700,
    "Previous Loan": "No",
    "Education": "Bachelor",
    "Home Onwership": "Rent",
    "Loan Intent": "Personal"
}

risk = predict_risk(test_data)

print("\nDefault Risk:", risk, "%")
print("Safety:", 100 - risk, "%")

result = get_decision(risk, 90)

print("\nFinal Decision:")
print(result)