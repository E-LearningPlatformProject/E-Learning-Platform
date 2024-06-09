from data.database import insert_query, read_query, update_query
from data.models import CoursesTagsResponeModel, CreateCourse, Course
from services import tags_service

def all_non_premium(search: str = None, skip: int = None, take: int = None):
    if search is None:
        data = read_query('''select c.id, c.title, c.description, c.level, c.image, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          where c.level = "public" and c.hidden = 0
                          group by c.title
                          order by c.id
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select c.id, c.title, c.description, c.level, c.image, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          join courses_has_tags as ct on c.id = ct.course_id
                          join tags as t on t.id = ct.tag_id 
                          where (level = "public" and c.hidden = 0) and c.title like ?
                          group by c.title
                          order by c.id
                          LIMIT ? ?''',(f'%{search}%', skip, take))
    
    
    return (CoursesTagsResponeModel.from_query_result(*row) for row in data)

def all_non_hidden(search: str = None, skip: int = None, take: int = None):
    if search is None:
        data = read_query('''select c.id, c.title, c.description, c.level, c.image, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          where c.hidden = 0
                          group by c.title
                          order by c.id
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select c.id, c.title, c.description, c.level, c.image, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          where c.hidden = 0 and c.title like ?
                          group by c.title
                          order by c.id
                          LIMIT ? ?''',(f'%{search}%', skip, take))
        
    return (CoursesTagsResponeModel.from_query_result(*row) for row in data)

def t_private(teacher_id, search:str = None, skip:int = None, take:int = None):
    if search is None:
        data = read_query('''select c.id, c.title, c.description, c.level, c.image, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id 
                          where author_id = ?
                          group by c.title
                          order by c.id
                          LIMIT ?, ?''', (teacher_id, skip, take))
    
    else:
        data = read_query('''select c.id, c.title, c.description, c.level, c.image, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id 
                          where c.title like ? and author_id = ?
                          group by c.title
                          order by c.id
                          LIMIT ? ?''',(f'%{search}%', teacher_id, skip, take))
        
    return (CoursesTagsResponeModel.from_query_result(*row) for row in data)

def all(search: str = None, skip: int = None, take: int = None):
    if search is None:
        data = read_query('''select c.id, c.title, c.description, c.level, c.image, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          group by c.title
                          order by c.id
                          LIMIT ?, ?''', (skip, take))
    
    else:
        data = read_query('''select c.id, c.title, c.description, c.level, c.image, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          where c.title like ?
                          group by c.title
                          order by c.id
                          LIMIT ? ?''',(f'%{search}%', skip, take))
        
    return (CoursesTagsResponeModel.from_query_result(*row) for row in data)


def create(course: CreateCourse, author_id:int):
    
    generated_id = insert_query(
        'insert into courses(title, description, level, author_id) values(?,?,?,?)',
        (course.title, course.description, course.level, author_id))

    course.id = generated_id
    
    tags = tags_service.get_tags_by_name(course.tags.split(','))
    tags_service.create(tags, generated_id)

    return course

def update(old: Course, new: Course):
    merged = Course(
        id=old.id,
        title=new.title or old.title,
        description=new.description or old.description,
        level=new.level or old.level,
        hidden= new.hidden or old.hidden,
        image=new.image or old.image,
        author_id=old.author_id,
        tags = new.tags or old.tags
        )

    update_query(
        '''UPDATE Courses
         SET
           title = ?, description = ?, level = ?, hidden = ?, image = ?
           WHERE id = ? 
        ''',
        (merged.title, merged.description, merged.level,merged.hidden, merged.image, merged.id))

    if new.tags != old.tags:
        tags_service.delete(old.id)
        tags = tags_service.get_tags_by_name(new.tags.split(','))
        tags_service.create(tags, old.id)

    return merged


def exists(id: int) -> bool:
    return any(
        read_query(
            'select id from courses where id = ?',
            (id,)))


def get_by_id(id: int):
    data = read_query('''select c.id, c.title, c.description, level, hidden, image, author_id, GROUP_CONCAT(t.title) as tags
                          from courses as c
                          left join courses_has_tags as ct on c.id = ct.course_id
                          left join tags as t on t.id = ct.tag_id
                          where c.id = ?
                          group by c.title''', (id,))

    return next((Course.from_query_result(*row) for row in data), None)

def sorting(courses: list[CoursesTagsResponeModel], *, attribute='', reverse=False):
    if attribute == 'title':
        def sorting_fn(c: CoursesTagsResponeModel): return c.title
    elif attribute != 'title' and attribute != None:
        def sorting_fn(c: CoursesTagsResponeModel): return c.tags if attribute in c.tags else c.tags
    else:
        def sorting_fn(c: CoursesTagsResponeModel): return c.id

    return sorted(courses, key=sorting_fn, reverse=reverse)

def get_course_authorID(course_id:int):
    data = read_query('''select author_id
                        from courses
                        where id = ?''', (course_id,))
    
    return data[0][0]

def is_hidden(id: int) -> bool:
    data = read_query(
            'select hidden from courses where id = ?',
            (id,))
    
    return True if data[0][0] == True else False

def delete(id):
    update_query('DELETE FROM courses WHERE id = ?', (id,))