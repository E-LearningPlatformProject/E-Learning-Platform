from data.database import insert_query, read_query, update_query
from data.models import CreateCourse, Course_UnAutUser, CourseResponseModel_StUser, CourseResponseModel_TchUser
from services.tags_service import get_tags_by_name

def all_non_private(search:str, skip:int, take:int):
    if search is None:
        data = read_query('''select id, title, description
                          from courses 
                          where level = "public"
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select id, title, description
                          from courses 
                          where level = "public" and name like ?
                          LIMIT ? ?''',(f'%{search}%', skip, take))
    
    return (Course_UnAutUser.from_query_result(*row) for row in data)
    return next((Course_UnAutUser(id=id, title=title, description=description) for id, title, description in data), None)

def all(search:str, skip:int, take:int):
    if search is None:
        data = read_query('''select id, title, description, level, author_id
                          from courses 
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select id, title, description, level, author_id
                          from courses 
                          where name like ?
                          LIMIT ? ?''',(f'%{search}%', skip, take))
        
    return (CourseResponseModel_StUser.from_query_result(*row) for row in data)

def t_private(search:str, teacher_id, skip:int, take:int):
    if search is None:
        data = read_query('''select id, title, description, level
                          from courses
                          where author_id = ?
                          LIMIT ?, ?''', (teacher_id, skip, take))
    
    else:
        data = read_query('''select id, title, description, level
                          from courses 
                          where name like ? and author_id = ?
                          LIMIT ? ?''',(f'%{search}%', teacher_id, skip, take))
        
    return (CourseResponseModel_TchUser.from_query_result(*row) for row in data)

def create(course: CreateCourse, author_id:int):
    
    generated_id = insert_query(
        'insert into courses(title, description, level, author_id) values(?,?,?,?)',
        (course.title, course.description, course.level, author_id))

    course_id = generated_id
    tags_name = []
    for tag in course.tags:
        tags_name.append(tag.title)
    tags = get_tags_by_name(tags_name)
    
    for tag_id in tags:
        insert_query(
            'insert into courses_has_tags(course_tag, tag_id) values(?,?)',
            (generated_id, tag_id))



    return course
