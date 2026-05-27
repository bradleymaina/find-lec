import sqlite3

db = sqlite3.connect("/home/nemo/find-lec/LecProfile/lecturer.db")
csr = db.cursor()

def search_lecturer():
    search_name = input("Enter Lecturer name: ")


    csr.execute("SELECT * FROM Lecturers WHERE name LIKE  ?", (f"%{search_name}%", ))

    results =  csr.fetchall()


    if results:
        print(f"\nFound {len(results)} matche(es)")
        print("-" * 40)

        for row in results:
            name = row[0]
            phone = row[1]

            display_phone = phone if phone else "[No Number Found]"

            print(f"Lecturer: {name}")
            print(f"Contact: {display_phone}")
            print("-" * 40)

    else:
        print("\nNot Found.")

if __name__  ==  "__main__":
    search_lecturer()
