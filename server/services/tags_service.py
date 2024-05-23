from data.database import insert_query, read_query, update_query
from data.models import Tag


def get_tags_by_course_id(course_id: int):
    data = read_query(
        '''SELECT t.id, t.title
            FROM tags as t
            join courses_has_tags as ct on t.id = ct.tag_id
            WHERE ct.course_id = ?''', (course_id,)
            )

    return (Tag.from_query_result(*row) for row in data)


def get_tags_by_name(tags: list):
    el = len(tags)
    data = read_query(
        f'''SELECT id
            FROM tags 
            WHERE title in ({(el * '?, ').removesuffix(', ')})''', tuple(tags)
            )
    
    return data

def create(tags: list, course_id:int):
    if tags:
        el = len(tags)
        CId_TId = []
        for tag_id in tags:
            CId_TId.extend([course_id,tag_id[0]])

        insert_query(
            f'''insert into courses_has_tags(course_id, tag_id) values
            {(el * '(?,?), ').removesuffix(', ')}''',
            tuple(CId_TId))
        
def delete(course_id:int):
    update_query('DELETE FROM courses_has_tags WHERE course_id = ?', (course_id,))
