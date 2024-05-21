from data.database import insert_query, read_query
from data.models import Role, StudentInfo, Students, TeacherInfo, User, Key
from mariadb import IntegrityError
from datetime import datetime, timezone, timedelta
import jwt
from hashlib import sha256


_EXP_TIME_TOKEN = 2

def _hash_password(password: str):

    return sha256(password.encode('utf-8')).hexdigest()


def find_by_email(email: str) -> User | None:
    data = read_query(
        'SELECT id, email, password, role FROM users WHERE email = ?',
        (email,))

    return next((User.from_query_result(*row) for row in data), None)


def find_student_info(email: str) -> User | None:
    data = read_query(
        '''
        SELECT students.id, users.email, users.password, users.role, students.first_name, students.last_name
        FROM users
        JOIN students ON users.id = students.users_id
        WHERE users.email = ?
        ''', (email,))
    
    return next((StudentInfo.from_query_result(*row) for row in data), None)


def find_teacher_info(email: str) -> User | None:
    data = read_query(
        '''
        SELECT teachers.id, users.email, users.password, users.role, teachers.first_name, teachers.last_name, teachers.phone_number, teachers.linked_in_account, teachers.is_approved
        FROM users
        JOIN teachers ON users.id = teachers.users_id
        WHERE users.email = ?
        ''', (email,))
    
    return next((TeacherInfo.from_query_result(*row) for row in data), None)


def try_login(email: str, password: str) -> User | None:
    user = find_by_email(email)

    hashed_password = _hash_password(password)

    return user if user and user.password == hashed_password else None


def create_student(email: str, password: str, first_name: str, last_name: str) -> User | None:
    
    hashed_password = _hash_password(password)

    try:
        generated_id = insert_query(
            'INSERT INTO users(email, password, role) VALUES (?,?,?)',
            (email, hashed_password, Role.STUDENT))

        generated_student_id = insert_query(
            'INSERT INTO students(users_id, first_name, last_name) VALUES (?,?,?)',
            (generated_id, first_name, last_name)
        )

        return User(id=generated_id, email=email, password='xxxxxxxxx', role=Role.STUDENT)
    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate usernames
        return None
    

def create_teacher(email: str, 
                   password: str, 
                   first_name: str, 
                   last_name: str,
                   phone_number,
                   linked_in_account) -> User | None:
    
    hashed_password = _hash_password(password)

    try:
        generated_id = insert_query(
            'INSERT INTO users(email, password, role) VALUES (?,?,?)',
            (email, hashed_password, Role.TEACHER))

        generated_teacher_id = insert_query(
            '''INSERT INTO teachers(users_id, first_name, last_name, phone_number, linked_in_account) 
            VALUES (?,?,?,?,?)''',
            (generated_id, first_name, last_name, phone_number, linked_in_account)
        )

        return User(id=generated_id, email=email, password='xxxxxxxxx', role=Role.TEACHER)
    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate usernames
        return None


def create_token(user: User) -> str:

    load = {"id":user.id,
           "email":user.email,
           "role":user.role,
           "iat": datetime.now(tz=timezone.utc),
           "exp":(datetime.now(tz=timezone.utc) + timedelta(hours=_EXP_TIME_TOKEN))
            }
    encoded = jwt.encode(payload = load, key = Key.KEY, algorithm="HS256")
   
    return encoded


def is_authenticated(token: str) -> bool:
    try:
        decoded = jwt.decode(token, Key.KEY, algorithms=["HS256"])
    
    except jwt.ExpiredSignatureError:
        return False

    return any(read_query(
        'SELECT 1 FROM users where id = ? and email = ?',
        (decoded['id'], decoded['email'])))


def from_token(token: str) -> User | None:
    try:
        decoded = jwt.decode(token, Key.KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    
    user = find_by_email(decoded['email'])
        
    if user.role == 'student':
        return find_student_info(decoded['email'])
    elif user.role == 'teacher':
        return find_teacher_info(decoded['email'])
    else:
        return find_by_email(decoded['email'])