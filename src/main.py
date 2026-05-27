import sqlite3

db = sqlite3.connect("lecturer.db")
csr = db.cursor()

csr.execute("CREATE TABLE IF NOT EXISTS Lecturers(name, phone_number)")


def get_lecturer_details(self):
    name = input("Name: ")
    phone = input("Phone_number: ")
    department = input ("Department: ")

   # if phone != 10:
    #    print("invalid number")
     #   break 
    

    csr.execute("INSERT INTO Lecturers VALUES (?, ?)", (name, phone_number))
    db.commit()
    db.close()
    


