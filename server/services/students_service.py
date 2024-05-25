from data.database import insert_query, read_query, update_query
from data.models import Enrollments, StudentInfo, Students, CreateCourse
from hashlib import sha256

def change_account_info(old: StudentInfo, new: StudentInfo):
    merged = StudentInfo(
        id= old.id,
        email= old.email,
        password= new.password or old.password,
        role= old.role,
        first_name= new.first_name or old.first_name,
        last_name= new.last_name or old.last_name
    )
    update_query(
        '''UPDATE users
        SET password = ?
        WHERE email = ? AND role = ?
        ''',
        (merged.password, merged.email, merged.role))
    update_query(
        '''UPDATE students
        SET first_name = ?, last_name = ?
        WHERE id = ?''',
        (merged.first_name, merged.last_name, merged.id))


    return merged


def enroll_student(course_id: int, student_id: int) -> Enrollments:
    insert_query('INSERT INTO enrollments (courses_id, students_id) VALUES (?, ?)', 
                (course_id, student_id))
                
    return 'Student\'s enrollment requested!'

def check_if_student_is_enrolled(course_id:int, student_id:int):
    return any(
        read_query(
            '''select courses_id, students_id 
            from enrollments 
            where courses_id = ? and students_id = ?''',
            (course_id, student_id)))
    
    



