import pandas as pd
import sqlite3

db = sqlite3.connect("/home/nemo/find-lec/LecProfile/lecturer.db")
csr = db.cursor()

#load new data
numbers_df = pd.read_csv("/home/nemo/find-lec/LecProfile/src/numbers.csv")

numbers_df['Name'] = numbers_df['Name'].str.strip().str.lower()

print(numbers_df)

print("Updating phone numbers...")


for index, row in numbers_df.iterrows():
    name = row['Name']
    phone = row ['Number']

    if pd.isna(phone):
        continue

    csr.execute ("""
        UPDATE Lecturers
        SET phone_number = ?
        WHERE LOWER(name) LIKE ?
    """, (phone, f"%{name}%"))

db.commit()
print(f"Update completed! {db.total_changes} rows were modified.")
db.close()
