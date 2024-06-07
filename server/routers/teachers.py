from typing import Optional
from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import LoginData, StudentInfo, Students, TeacherInfo, Teachers, User
from services import teachers_service

teachers_router = APIRouter(prefix='/teachers', tags=['Teachers'])

@teachers_router.put('/', response_model=TeacherInfo)
def update_teacher_info(teacher: TeacherInfo,  x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You should have registration!')
    existing_teacher = get_user_or_raise_401(x_token)
    return teachers_service.change_account_info(existing_teacher, teacher)
    