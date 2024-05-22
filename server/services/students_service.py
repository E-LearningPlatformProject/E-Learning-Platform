from data.database import insert_query, read_query, update_query
from data.models import Role, StudentInfo
from hashlib import sha256

def change_account_info(old: StudentInfo, new: StudentInfo):
    merged = StudentInfo(
        id= old.id,
        email= old.email,
        password= new.password or old.password,
        role= old.role,
        first_name= new.first_name or old.first_name,
        last_name= new.last_name or old.last_name
    )
    update_query(
        '''UPDATE users
        SET password = ?
        WHERE email = ? AND role = ?
        ''',
        (merged.password, merged.email, merged.role))
    update_query(
        '''UPDATE students
        SET first_name = ?, last_name = ?
        WHERE id = ?''',
        (merged.first_name, merged.last_name, merged.id))


    return merged

