

import mysql.connector
from datetime import datetime
from REAL_TIME_FACE_DETECTION import detected_faces


db = mysql.connector.connect(user='admin',
                               password='#BRSOmkar123',
                               host='localhost',
                               database='attendance_system')

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
day_of_week = now.strftime('%A')
date_string = now.strftime("%Y-%m-%d")


def mark_attendance(student_id):
    if detected_faces:

        for index in recognized_student_id:

            student_id=index
            cursor1 = db.cursor(buffered=True)

            try:

                cursor1.execute(
                    "SELECT subject_name FROM timetable WHERE day_of_week = %s AND start_time <= %s AND end_time >= %s",
                    (day_of_week, current_time, current_time))

                subject_result = cursor1.fetchone()

                if subject_result:
                    current_subject = subject_result[0]

                    cursor1.execute("""
                        INSERT INTO attendance (student_id, date, subject_name, day_of_week,status) 
                        VALUES (%s, %s, %s,%s, 'Present')
                        ON DUPLICATE KEY UPDATE status = 'present'
                    """, (student_id, date_string, current_subject,day_of_week))

                    db.commit()

                    print(f'Attendance marked for student {student_id} for {current_subject} on {date_string} ({day_of_week}).')
                    if absent_student_id:
                        for student in absent_student_id:
                            student_id=student
                            cursor1.execute("""
                                             INSERT INTO attendance (student_id, date, subject_name, day_of_week,status) 
                                             VALUES (%s, %s, %s,%s, 'Absent')
                                            """, (student_id, date_string, current_subject, day_of_week))
                            db.commit()

                else:
                    print("No class currently scheduled.")



            except mysql.connector.errors.IntegrityError:
                print(f'Attendance for {date_string} already exists.')


            finally:
                cursor1.close()
    else:
        cursor2 = db.cursor(buffered=True)

        try:

            cursor2.execute(
                "SELECT subject_name FROM timetable WHERE day_of_week = %s AND start_time <= %s AND end_time >= %s",
                (day_of_week, current_time, current_time))

            subject_result = cursor2.fetchone()

            if subject_result:
                current_subject = subject_result[0]
                for student in list_of_student_id:
                    student_id = student
                    print(f'Attendance marked for student {student_id} for {current_subject} on {date_string} ({day_of_week}).')
                    cursor2.execute("""
                                             INSERT INTO attendance (student_id, date, subject_name, day_of_week,status)
                                             VALUES (%s, %s, %s,%s, 'Absent')
                                            """, (student_id, date_string, current_subject, day_of_week))
                    db.commit()
            else:
                print("No class currently scheduled.")
        except mysql.connector.errors.IntegrityError:
            print(f'Attendance for {date_string} already exists.')

        finally:
            cursor2.close()





recognized_student_id = detected_faces
recognized_student_id = [int(num) for num in recognized_student_id]
list_of_student_id=[1,2,3,4]
absent_student_id=[]
for index in list_of_student_id:
    if index not in recognized_student_id:
        absent_student_id.append(index)

mark_attendance(recognized_student_id)

db.close()