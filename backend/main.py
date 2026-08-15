from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.auth import router as auth_router
from backend.routes.employees import router as employee_router
from backend.routes.risk_settings import router as risk_router
from backend.routes.prediction import router as prediction_router

app = FastAPI(title="Loan Default Risk Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://loan-default-project-xg3b.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(risk_router)
app.include_router(prediction_router)


@app.get("/")
def home():
    return {
        "message": "Loan Default Risk Management System is running"
    }