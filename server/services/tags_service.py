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
    return next((Tag(title=title) for title in data), None)

def get_tags_by_name(tags: list):
    data = read_query(
        '''SELECT id
            FROM tags 
            WHERE title in (?)''', (tuple(tags),)
            )
    
    return data