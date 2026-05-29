# this module is aimed at obtaining a structured information from 
# users to update database

import sqlite3

#clean_lecturer.db is a new databse that is meant to obtain
#current lecturer details in a neat form as compared to 
#scrapped data from the previous lecturer.db

def get_lecturer_details():
    db = sqlite3.connect("clean_lecturer.db")
    csr = db.cursor()

    print("Do not Include Titles such as Dr/Mr when entering name!")
    print("Begin with the English  Name !")

    while True:
        first_name = input("\nEnter First Name (or 'quit' to exit): ").strip().title()
        if first_name.lower() == 'quit':
            break

        last_name = input("Enter Last Name:   ").strip().title()
        if last_name.lower() == 'quit':
            break

        print("Phone numbers should be in the format 07********")

        # Added .strip() here as requested
        phone_number = input("Enter Phone Number: ").strip()
        if phone_number.lower() == 'quit':
            break
    
        # Changed return to continue so the loop keeps running after an error
        if len(phone_number) <  10 :
            print("The phone number is too short!")
            continue
        elif len(phone_number) > 10:
            print("The phone number is too long!")
            continue

        # Create table
        csr.execute("""
        CREATE TABLE IF NOT EXISTS 
        lecturer_table(first_name TEXT, last_name TEXT , phone_number TEXT)
        """)

        print("Saving to database...")
    
        csr.execute("INSERT INTO lecturer_table VALUES (?, ?, ?)", (first_name, last_name, phone_number))

        print(f"{first_name} {last_name} with phone number {phone_number} has been updated to the database")

        db.commit()

    # db.close() is now outside the loop
    print("Exiting and closing database.")
    db.close()

    
if __name__ == "__main__":
    get_lecturer_details()
