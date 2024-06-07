from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest
from data.models import LoginData, Students, Teachers, User, AdminEmail
from services import users_service, teachers_service
from data.send_mail import send_email
from pathlib import Path
from fastapi.responses import FileResponse


users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/login')
def login(data: LoginData):
    
    user = users_service.try_login(data.email, data.password)

    if user:
        token = users_service.create_token(user)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')


@users_router.get('/info', response_model=User)
def user_info(x_token: str | None = Header()):
    if  not x_token :
        return BadRequest('No No')
    
    user = get_user_or_raise_401(x_token)

    image = Path(user.image)
    
    image_res = FileResponse(image)
    return  user, image_res


@users_router.post('/register/student', response_model=User)
def register(user_data: User, student_data: Students):

    if user_data.email and user_data.password:
        user = users_service.create_student(user_data.email, user_data.password, student_data.first_name, student_data.last_name)
    else:
        if not user_data.email:
            return BadRequest(content= 'Email should contain symbol "@" and at least one full stop "."')
        if not user_data.password:
            return BadRequest(content= 'Password should be between 6 and 30 symbols.')
    
    return user or BadRequest(f'Email {user_data.email} is taken.')


@users_router.post('/register/teacher', response_model=User)
def register(user_data: User, teacher_data: Teachers):
    teacher_data.image = teachers_service.resize_image(teacher_data.image,teacher_data.first_name, teacher_data.last_name)

    if user_data.email and user_data.password:
        user = users_service.create_teacher(user_data.email,
                                            user_data.password,
                                            teacher_data.first_name, 
                                            teacher_data.last_name,
                                            teacher_data.phone_number,
                                            teacher_data.linked_in_account,
                                            teacher_data.image)
    else:
        if not user_data.email:
            return BadRequest(content= 'Email should contain symbol "@" and at least one full stop "."')
        if not user_data.password:
            return BadRequest(content= 'Password should be between 6 and 30 symbols.')
        
    if user:
        send_email(AdminEmail._EMAIL, user_data.email, user.id)
    
    return user or BadRequest(f'Email {user_data.email} is taken.')