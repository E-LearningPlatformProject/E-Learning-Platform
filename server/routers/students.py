from typing import Optional
from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import LoginData, StudentInfo, Students, Teachers, User
from services import students_service

students_router = APIRouter(prefix='/students')

@students_router.put('/')
def update_student_info(student: StudentInfo,  x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You should have registration!')
    existing_student = get_user_or_raise_401(x_token)
    return students_service.change_account_info(existing_student, student)
    