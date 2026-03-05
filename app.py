from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# -----------------------
# DATABASE CONNECTION
# -----------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Enhypen_bts@2",  # CHANGE THIS
        database="hospital_db"
    )

# -----------------------
# HOME ROUTE
# -----------------------
@app.route("/")
def home():
    return "🏥 Hospital Backend Running Successfully"

# -----------------------
# GET ALL PATIENTS
# -----------------------
@app.route("/patients", methods=["GET"])
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Patients")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# -----------------------
# ADD NEW PATIENT
# -----------------------
@app.route("/patients", methods=["POST"])
def add_patient():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO Patients (age, gender, blood_type)
        VALUES (%s, %s, %s)
    """

    values = (
        data["age"],
        data["gender"],
        data["blood_type"]
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Patient added successfully"}), 201

# -----------------------
# GENDER ANALYTICS
# -----------------------
@app.route("/analytics/gender", methods=["GET"])
def gender_analytics():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT gender, COUNT(*) as count
        FROM Patients
        GROUP BY gender
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)

# -----------------------
# BILLING ANALYTICS
# -----------------------
@app.route("/analytics/billing", methods=["GET"])
def billing_analytics():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT admission_type, AVG(billing_amount) as avg_billing
        FROM Visits
        GROUP BY admission_type
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)

# -----------------------
# RISK CLASSIFICATION
# -----------------------
@app.route("/analytics/risk", methods=["GET"])
def risk_distribution():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT age FROM Patients")
    patients = cursor.fetchall()

    high = 0
    medium = 0
    low = 0

    for p in patients:
        if p["age"] > 60:
            high += 1
        elif 40 <= p["age"] <= 60:
            medium += 1
        else:
            low += 1

    cursor.close()
    conn.close()

    return jsonify({
        "High Risk": high,
        "Medium Risk": medium,
        "Low Risk": low
    })

# -----------------------
# SEARCH FILTER
# Example: /search?gender=Male
# -----------------------
@app.route("/search", methods=["GET"])
def search_patients():
    gender = request.args.get("gender")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if gender:
        cursor.execute("SELECT * FROM Patients WHERE gender = %s", (gender,))
    else:
        cursor.execute("SELECT * FROM Patients")

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(data)

# -----------------------
# RUN SERVER
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)