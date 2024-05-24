from data.database import insert_query, read_query, update_query
from data.models import Section

def create(section: Section, course_id):

    generated_id = insert_query(
        'insert into sections(title, type_file, course_id, source) values(?,?,?,?)',
        (section.title, section.type_file, course_id, section.source))

    section.id = generated_id
    section.course_id = course_id

    return section

def get_sections(course_id:int):
    data = read_query('''select id, title, type_file, course_id, source
                        from sections
                        where COURSE_id = ?''', (course_id,))
    
    return (Section.from_query_result(*row) for row in data)

def get_by_id(id: int):

    data = read_query('''select id, title, type_file, course_id, source
                        from sections
                        where id = ?''', (id,))
    
    return next((Section.from_query_result(*row) for row in data), None)

def update(old:Section, new:Section):
    merged = Section(
        id=old.id,
        title=new.title or old.title,
        type_file=new.type_file or old.type_file,
        course_id=old.course_id,
        source= new.source or old.source,
        )

    update_query(
        '''UPDATE Sections
         SET
           title = ?,  type_file = ?, source = ?
           WHERE id = ? 
        ''',
        (merged.title, merged.type_file, merged.source, merged.id))
    
    return merged


def check_if_student_is_enrolled(course_id:int, student_id:int):
    return any(
        read_query(
            '''select courses_id, students_id 
            from enrollments 
            where courses_id = ? and students_id = ?''',
            (course_id, student_id)))
