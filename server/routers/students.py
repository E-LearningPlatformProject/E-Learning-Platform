from typing import Optional
from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, Forbidden, Unauthorized
from data.models import Role, StudentInfo
from data.send_mail import send_email
from services import students_service, courses_service, teachers_service


students_router = APIRouter(prefix='/students')

@students_router.put('/')
def update_student_info(student: StudentInfo,  x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You should have registration!')
    existing_student = get_user_or_raise_401(x_token)
    return students_service.change_account_info(existing_student, student)

    
@students_router.post('/enrolment/{course_id}')
def enroll_student_into_course(course_id: int, x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You should have registration!')
    
    if not courses_service.exists(course_id):
        return BadRequest('Course doesn\'t exist!')
    
    existing_student = get_user_or_raise_401(x_token)
    if existing_student.role != Role.STUDENT:
        return Forbidden('You should be a student to enroll!')
    
    send_email(teachers_service.get_teacher_email(course_id),existing_student.email, existing_student.id)
   
    return students_service.enroll_student(course_id, existing_student.id)

