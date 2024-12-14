import streamlit as st
import mysql.connector
import pandas as pd
import bcrypt


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='admin',
        password='#BRSOmkar123',
        database='attendance_system'
    )


def fetch_user(username):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user


def fetch_students():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT username FROM users WHERE role = 'student'")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return [student['username'] for student in students]

def fetch_total_classes(subject, month):
    db = get_db_connection()
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM Attendance WHERE subject_name = %s AND MONTH(date) = %s"
    cursor.execute(query, (subject, month))
    total_classes = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return total_classes

def calculate_attendance_percentage_by_student(month):
    db = get_db_connection()
    cursor = db.cursor()

    query = """
    SELECT student_id, 
           COUNT(*) as total_classes, 
           SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_classes
    FROM Attendance
    WHERE MONTH(date) = %s
    GROUP BY student_id
    """
    cursor.execute(query, (month,))
    data = cursor.fetchall()

    attendance_percentages = []
    defaulters = []


    for row in data:
        student_id, total_classes, present_classes = row
        if total_classes > 0:

            attendance_percentage = (present_classes / total_classes) * 100
            attendance_percentages.append({
                'student_id': student_id,
                'total_classes': total_classes,
                'present_classes': present_classes,
                'attendance_percentage': attendance_percentage
            })

            # Check if the student is a defaulter (attendance < 70%)
            if attendance_percentage < 70:
                defaulters.append({
                    'student_id': student_id,
                    'attendance_percentage': attendance_percentage
                })

    cursor.close()
    db.close()

    return attendance_percentages, defaulters




def fetch_attendance(role, username=None, subject=None, month=None, date=None):
    db = get_db_connection()
    cursor = db.cursor()

    query = "SELECT * FROM Attendance WHERE 1=1"
    params = []


    if role == 'teacher' and username:
        query += " AND student_id = %s"
        params.append(username)
    elif role == 'student':
        query += " AND student_id = %s"
        params.append(username)

    if subject:
        query += " AND subject_name = %s"
        params.append(subject)

    if month:
        query += " AND MONTH(date) = %s"
        params.append(month)

    if date:
        query += " AND date = %s"
        params.append(date)

    # Execute the query with the parameters
    cursor.execute(query, params)
    columns = cursor.column_names
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=columns)



def register_user(username, password, role):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    db.commit()
    cursor.close()
    db.close()
    st.success("User registered successfully!")


st.title("Smart Attendance System")

with st.sidebar:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        role = st.selectbox("Select Role", ["teacher", "student"], key="login_role")

        if st.button("Login"):
            user = fetch_user(username)
            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    if user['role'] == role:
                        st.session_state['username'] = username
                        st.session_state['role'] = user['role']
                        st.session_state['logged_in'] = True
                        st.success(f"Logged in as {username} ({user['role']})")
                    else:
                        st.error("Role does not match. Please select the correct role.")
                else:
                    st.error("Invalid password. Please try again.")
            else:
                st.error("User not found. Please check your username.")

    with tab2:
        st.header("Sign Up")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')
        new_role = st.selectbox("Select Role", ["teacher", "student"], key="signup_role")

        if st.button("Sign Up"):
            if new_username and new_password:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                register_user(new_username, hashed_password, new_role)
            else:
                st.warning("Please fill in all fields.")

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    # Filters
    month = st.selectbox("Select Month", [None] + list(range(1, 13)),
                         format_func=lambda x: f"{x:02d}" if x else "All Months")
    date = st.date_input("Select Date", None)

    if st.session_state['role'] == 'teacher':
        # Fetch the list of students
        students = fetch_students()
        student_username = st.selectbox("Select Student", [None] + students)

        # Display Attendance Records
        attendance_data = fetch_attendance(st.session_state['role'],
                                           student_username if student_username else None,
                                           None,  # No subject filter
                                           month if month else None,
                                           date if date else None)
        st.write("Attendance Records:")
        st.dataframe(attendance_data)

        # Show the Calculate Attendance Percentage button only if a month is selected
        if month:
            if st.button("Calculate Attendance Percentage"):
                # Call function to calculate attendance percentage for all students in the selected month
                attendance_percentages, defaulters = calculate_attendance_percentage_by_student(month)

                # Display Attendance Percentages
                if attendance_percentages:
                    st.write("Attendance Percentages (By Student):")
                    df_attendance = pd.DataFrame(attendance_percentages)
                    st.dataframe(df_attendance)
                else:
                    st.warning("No attendance data found for the selected month.")

                # Display Defaulters (Attendance < 70%)
                if defaulters:
                    st.warning("Defaulters (Attendance < 70%):")
                    st.write(defaulters)
                else:
                    st.success("No defaulters for this month.")
        else:
            st.warning("Please select a month to calculate attendance percentages.")

    else:
        # For students, only show their own attendance records
        attendance_data = fetch_attendance(st.session_state['role'],
                                           st.session_state['username'],
                                           None,  # No subject filter
                                           month if month else None,
                                           date if date else None)

        st.write("Attendance Records:")
        st.dataframe(attendance_data)


