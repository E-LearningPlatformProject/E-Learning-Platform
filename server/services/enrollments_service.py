from data.database import insert_query, read_query, update_query


def delete(course_id):
    update_query('DELETE FROM enrollments WHERE courses_id = ?', (course_id,))