from data.database import insert_query, read_query, update_query


def delete(course_id):
    update_query('DELETE FROM enrollments WHERE courses_id = ?', (course_id,))

def find_enrolled_students_in_course(course_id):
    data = read_query('''select u.email
                      from enrollments as e
                      join students as s on s.id = e.students_id
                      join users as u on u.id = users_id 
                      where e.courses_id = ?''',(course_id,))
    
    students_email = [e[0] for e in data]
    print(students_email)

    return students_email