import pandas as pd
import mysql.connector


df = pd.read_excel("hospital_data.xlsx")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Enhypen_bts@2",
    database="hospital_db"
)

cursor = conn.cursor()

for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Patients (age, gender, blood_type)
        VALUES (%s, %s, %s)
    """, (row['Age'], row['Gender'], row['Blood Type']))

conn.commit()
conn.close()

print("Data inserted successfully!")