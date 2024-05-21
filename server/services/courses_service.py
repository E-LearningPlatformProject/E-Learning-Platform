from data.database import insert_query, read_query, update_query
from data.models import CoursesTagsResponeModel, CreateCourse, CourseResponseModel_StUser, CourseResponseModel_TchUser
from services.tags_service import get_tags_by_name

def all_non_premium(search:str, skip:int, take:int):
    if search is None:
        data = read_query('''select c.id, c.title, c.description, level, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          where c.level = "public" and c.hidden = 0
                          group by c.title
                          order by c.id
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select c.id, c.title, c.description, level, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          join courses_has_tags as ct on c.id = ct.course_id
                          join tags as t on t.id = ct.tag_id 
                          where (level = "public" and c.hidden = 0) and c.title like ?
                          group by c.title
                          order by c.id
                          LIMIT ? ?''',(f'%{search}%', skip, take))
    
    
    return (CoursesTagsResponeModel.from_query_result(*row) for row in data)

def all_non_hidden(search:str, skip:int, take:int):
    if search is None:
        data = read_query('''select c.id, c.title, c.description, level, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          where c.hidden = 0
                          group by c.title
                          order by c.id
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select c.id, c.title, c.description, level, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          join courses_has_tags as ct on c.id = ct.course_id
                          join tags as t on t.id = ct.tag_id
                          where c.hidden = 0 and c.title like ?
                          group by c.title
                          order by c.id
                          LIMIT ? ?''',(f'%{search}%', skip, take))
        
    return (CoursesTagsResponeModel.from_query_result(*row) for row in data)

def t_private(search:str, teacher_id, skip:int, take:int):
    if search is None:
        data = read_query('''select c.id, c.title, c.description, level, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          join courses_has_tags as ct on c.id = ct.course_id
                          join tags as t on t.id = ct.tag_id 
                          where author_id = ?
                          group by c.title
                          order by c.id
                          LIMIT ?, ?''', (teacher_id, skip, take))
    
    else:
        data = read_query('''select c.id, c.title, c.description, level, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          join courses_has_tags as ct on c.id = ct.course_id
                          join tags as t on t.id = ct.tag_id 
                          where c.title like ? and author_id = ?
                          group by c.title
                          order by c.id
                          LIMIT ? ?''',(f'%{search}%', teacher_id, skip, take))
        
    return (CoursesTagsResponeModel.from_query_result(*row) for row in data)

def all(search:str, skip:int, take:int):
    if search is None:
        data = read_query('''select c.id, c.title, c.description, level, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          group by c.title
                          order by c.id
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select c.id, c.title, c.description, level, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          join courses_has_tags as ct on c.id = ct.course_id
                          join tags as t on t.id = ct.tag_id
                          where c.title like ?
                          group by c.title
                          order by c.id
                          LIMIT ? ?''',(f'%{search}%', skip, take))
        
    return (CoursesTagsResponeModel.from_query_result(*row) for row in data)


def create(course: CreateCourse, author_id:int):
    
    generated_id = insert_query(
        'insert into courses(title, description, level, author_id) values(?,?,?,?)',
        (course.title, course.description, course.level, author_id))

    course_id = generated_id
    
    tags = get_tags_by_name(course.tags.split(','))
    if tags:
        el = len(tags)
        CId_TId = []
        for tag_id in tags:
            CId_TId.extend([generated_id,tag_id[0]])

        insert_query(
            f'''insert into courses_has_tags(course_id, tag_id) values
            {(el * '(?,?), ').removesuffix(', ')}''',
            tuple(CId_TId))



    return course
