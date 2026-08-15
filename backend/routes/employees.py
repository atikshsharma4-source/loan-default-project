from fastapi import APIRouter, HTTPException
from backend.database.connection import connection
router = APIRouter()
@router.post("/signup")
def signup(name: str, email: str, password: str):
    cursor = connection.cursor()
    query = """INSERT INTO employees (name, email, password)
     VALUES (%s, %s, %s)"""
    values = (name, email, password)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    return {
        "message": "Employee created successfully"
    }

@router.post("/login")
def login(email: str, password: str):

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, name, email
        FROM employees
        WHERE email = %s AND password = %s
    """

    values = (email, password)

    cursor.execute(query, values)

    employee = cursor.fetchone()

    cursor.close()

    if not employee:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "employee": employee
    }


@router.get("/employees")
def get_employees():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM employees"
    cursor.execute(query)
    employees = cursor.fetchall()
    cursor.close()
    return employees
@router.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    name: str,
    email: str,
    password: str
):
    cursor = connection.cursor()
    query = """
        UPDATE employees
        SET name = %s,
            email = %s,
            password = %s
        WHERE id = %s
    """
    values = (name, email, password, employee_id)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    return {
        "message": "Employee updated successfully"
    }
@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    cursor = connection.cursor()
    query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(query, (employee_id,))
    connection.commit()
    cursor.close()
    return {
        "message": "Employee deleted successfully"
    }


