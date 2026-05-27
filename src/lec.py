#this module obtains lecturer details from 
#an examination timetable 
#the lecturer details obtained are the names only .
#the lecturer details are from Bachelor's degree lecturers only 

import pdfplumber
import pandas as pd
import sqlite3

db = sqlite3.connect("/home/nemo/find-lec/LecProfile/lecturer.db")
csr = db.cursor()

csr.execute("CREATE TABLE IF NOT EXISTS Lecturers(name TEXT UNIQUE, phone_number TEXT)")

#get the number of pages in the pdf
with pdfplumber.open("/home/nemo/datasets/timetable.pdf") as pdf:
    all_rows = []
    headers = None


    total_pages = len(pdf.pages)
   # print(total_pages)

#extract the tables from all the pages in the pdf
# Add logic for when pdf and/or table does not exist
    for page in pdf.pages:
        table = page.extract_table()
        if not table:
            continue

        if headers is None:
            # Smart Header Detection: Find the row that actually contains labels
            for i, row in enumerate(table):
                # Clean the row to check for keywords accurately
                clean_row = [str(cell).strip() if cell else "" for cell in row]
                if "LECTURER" in clean_row or "COURSE" in clean_row:
                    headers = clean_row
                    all_rows.extend(table[i+1:])
                    break
        else:
            all_rows.extend(table)

    # Move DataFrame creation outside the loop for efficiency
    df = pd.DataFrame(all_rows, columns=headers)

    #data cleaning
    #remove whitespaces
    df = df.apply (lambda x: x.str.strip() if x.dtype == "object" else x)

    #remove rows where the lecturer is missing 
    df = df.dropna(subset=["LECTURER"])

    #filter out rows that are empty strings
    df = df[df["LECTURER"] != ""]
    df = df[df["LECTURER"] != "LECTURER" ]

    teachers = df["LECTURER"].unique()
    count = len(teachers)

       

    pd.set_option('display.max_rows', None)
    print(pd.Series(teachers))
    print(f"Lecturers:{count}")


    #move data from RAM to SSD
    print("SAVING TO DATABASE...")
    
    for name in teachers:
        csr.execute("INSERT INTO Lecturers (name) VALUES (?)", (name, ))

    db.commit()
    print("Completed")
    db.close()
   


        
