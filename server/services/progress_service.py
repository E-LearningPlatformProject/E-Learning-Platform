from data.database import insert_query, read_query, update_query
from data.models import Section
from services import sections_service

def create(student_id, sections_id):
    insert_query(
        '''INSERT INTO progress (students_id, sections_id)
            SELECT ?, ?
            WHERE NOT EXISTS (
            SELECT students_id, sections_id 
            FROM progress 
            WHERE students_id = ? and sections_id = ?)''',
        (student_id, sections_id, student_id, sections_id))
    

def progress(student_id, course_id):
    data = read_query('''select ROUND(((select count(concat(students_id, sections_id)) as num
		            from progress
		            where students_id = ? and sections_id in (select id from sections where course_id = ?)) 
                      / count(s.id))*100) as progress
                    from sections as s
                    where s.course_id=?''',(student_id,course_id,course_id))
    
    return data[0][0]


def exists(section_id: int) -> bool:
    return any(
        read_query(
            'SELECT sections_id FROM progress WHERE sections_id = ?',
            (section_id,)))


def remove_progress_by_section(section_id):
    update_query('DELETE FROM progress WHERE sections_id = ?', (section_id,))
    