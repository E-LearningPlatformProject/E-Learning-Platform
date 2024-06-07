from data.database import insert_query, read_query, update_query
from data.models import TeacherInfo, Route
from PIL import Image


def change_account_info(old: TeacherInfo, new: TeacherInfo):
    merged = TeacherInfo(
        id= old.id,
        email= old.email,
        password= new.password or old.password,
        role= old.role,
        first_name= new.first_name or old.first_name,
        last_name= new.last_name or old.last_name,
        phone_number= new.phone_number or old.phone_number,
        linked_in_account= new.linked_in_account or old.linked_in_account,
        is_approved= old.is_approved
    )
    update_query(
        '''UPDATE users
        SET password = ?
        WHERE email = ? AND role = ?
        ''',
        (merged.password, merged.email, merged.role))
    update_query(
        '''UPDATE teachers
        SET first_name = ?, last_name = ?, phone_number = ?, linked_in_account = ?
        WHERE id = ? AND is_approved = ?''',
        (merged.first_name, merged.last_name, merged.phone_number, merged.linked_in_account, merged.id, merged.is_approved))

    return merged

def check_if_is_approved(teacher_id):
    data = read_query('''select is_approved
                      from teachers
                      where id = ?''',(teacher_id,))
    
    return True if data[0][0]== 1 else False

def get_teacher_email(course_id):
    data = read_query('''select email
                from users as u
                join teachers as t on u.id = t.users_id
                join courses as c on c.author_id = t.id
                where c.id = ?''', (course_id,))
    
    return data[0][0]

def resize_image(path:str, first_name, last_name):
    image = Image.open(path)
    new_image = image.resize((400, 500))
    
    new_path = Route.ROUTE_TEACH_IMAGES + first_name + '_' + last_name+'.png'
    new_image.save(new_path)

    return new_path