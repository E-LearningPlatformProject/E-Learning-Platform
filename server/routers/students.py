from typing import Optional
from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, Forbidden, Unauthorized, Ok
from data.models import Role, StudentInfo, Vote, Enrollments
from data.send_mail import send_email
from services import students_service, courses_service, teachers_service, progress_service, ratings_service


students_router = APIRouter(prefix='/students', tags=['Students'])

@students_router.put('/', response_model=StudentInfo)
def update_student_info(student: StudentInfo,  x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You should have registration!')
    existing_student = get_user_or_raise_401(x_token)
    return students_service.change_account_info(existing_student, student)

    
@students_router.post('/enrolment/{course_id}', response_model= Enrollments)
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


@students_router.get('/progress/{course_id}')
def get_progress(course_id: int, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('You should have registration!')
    
    if not courses_service.exists(course_id):
        return BadRequest('Course doesn\'t exist!')
    
    user = get_user_or_raise_401(x_token)

    if user.role == Role.STUDENT:
        
        if not students_service.check_if_student_is_enrolled(course_id, user.id):
            return Unauthorized('You aren\'t enrolled in this course!')

        return Ok(f'Your progress is {progress_service.progress(user.id, course_id)}% for Course with ID: {course_id}')

    else:
        return Forbidden('Only students can view their progress!')
    
@students_router.post('/rating')
def vote(vote:Vote, x_token: Optional[str] = Header(None)):

    if not x_token:
        return Unauthorized('You should have registration!')
    
    if not courses_service.exists(vote.course_id):
        return BadRequest(F'Course with ID: {vote.course_id} doesn\'t exist!')
    
    if vote.rating==0:
        return BadRequest('Your vote must be betweeen 1 and 10')
    user = get_user_or_raise_401(x_token)

    if user.role == Role.STUDENT:
        if not students_service.check_if_student_is_enrolled(vote.course_id, user.id):
            return Unauthorized('You aren\'t enrolled in this course!')
        
        if ratings_service.check_if_student_had_vote(vote.course_id, user.id):
            return Forbidden('You can\'t change your vote!')
        
        ratings_service.vote(vote, user.id)

        return Ok('Your vote was seccesfull!')

    else:
        return Forbidden('Only students can vote!')
    
@students_router.get('/avg_rating/{course_id}')
def get_avg(course_id):
    return ratings_service.average_rating(course_id)

