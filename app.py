
# Application: Student Database CRUD Operations
#   Connects to a PostgreSQL database and performs
#   Create, Read, Update, Delete operations on the 'students' table.


import psycopg2
from psycopg2 import sql
from datetime import date


DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",          
    "password": "sqlsujay",    
    "database": "students_db"    
}

# function to connect to the database
def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(" Error connecting to the database:", e)
        return None


# Get students information and display
def getAllStudents():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT * From students order by student_id;")
        rows = cur.fetchall()
        print("\n All Students:")
        print("----------------------------------------------------")
        for row in rows:
            print(f"ID: {row[0]} | {row[1]} {row[2]} | Email: {row[3]} | Enrolled: {row[4]}")
        print("----------------------------------------------------\n")
        cur.close()
    except Exception as e:
        print(" Error fetching students:", e)
    finally:
        conn.close()


# Add a new student to the database
def addStudent(first_name, last_name, email, enrollment_date):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id;
        """, (first_name, last_name, email, enrollment_date))
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"Student added successfully with ID: {new_id}")
        cur.close()
    except Exception as e:
        print(" Error adding student:", e)
    finally:
        conn.close()


#  Update a student’s email already in the database
def updateStudentEmail(student_id, new_email):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE students
            SET email = %s
            WHERE student_id = %s;
        """, (new_email, student_id))
        if cur.rowcount == 0:
            print(" No student found with that ID.")
        else:
            conn.commit()
            print(" Student email updated successfully.")
        cur.close()
    except Exception as e:
        print(" Error updating student email:", e)
    finally:
        conn.close()


# Delete a student from the database
def deleteStudent(student_id):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("Delete from students WHERE student_id = %s;", (student_id,))
        if cur.rowcount == 0:
            print(" No student found with that ID.")
        else:
            conn.commit()
            print("Student deleted successfully.")
        cur.close()
    except Exception as e:
        print(" Error deleting student:", e)
    finally:
        conn.close()


# Display menu
def menu():
    while True:
        print("""
        ===== STUDENT DATABASE MENU =====
        1. View all students
        2. Add a new student
        3. Update student email
        4. Delete a student
        5. Exit
        =================================
        """)
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            getAllStudents()
        elif choice == "2":
            fn = input("First name: ")
            ln = input("Last name: ")
            em = input("Email: ")
            date_str = input("Enrollment date (YYYY-MM-DD): ")
            addStudent(fn, ln, em, date_str)
        elif choice == "3":
            sid = input("Enter student ID to update: ")
            new_em = input("New email: ")
            updateStudentEmail(sid, new_em)
        elif choice == "4":
            sid = input("Enter student ID to delete: ")
            deleteStudent(sid)
        elif choice == "5":
            print(" Exiting program. Goodbye!")
            break
        else:
            print(" Invalid choice, please try again.")


if __name__ == "__main__":
    menu()
