#this module is to find out how many lecturers have contact details and 
#how many lecturers do not have contact details updated

import sqlite3

db = sqlite3.connect("/home/nemo/find-lec/LecProfile/lecturer.db")
csr = db.cursor()

#execute sql querry to find out 
query = """
SELECT name 
FROM Lecturers
WHERE phone_number IS  NULL OR phone_number == '' ;
 """
csr.execute(query)

results = csr.fetchall()

if results:
     print("Lecturers without contact details")
     for row in results:
         print(row[0])
else:
    print("No Lectureres without contact details")

count = len(results)
print(f"{count} Lecturers currently have no contact details assigned to them")


db.close()


