from typing import Optional
from fastapi import APIRouter, Header
from pydantic import BaseModel
from common.responses import BadRequest, Forbidden, NotFound, Unauthorized, Ok
from common.auth import get_user_or_raise_401
from services import courses_service, teachers_service, sections_service, enrollments_service, ratings_service, tags_service, progress_service
from data.models import Role, CreateCourse, Course, CourseSectionsResponseModel, CoursesTagsResponeModel
from data.send_mail import send_email
from PIL import Image
from fastapi.responses import FileResponse
from pathlib import Path


courses_router = APIRouter(prefix='/courses', tags=['Courses'])

@courses_router.get('/', response_model= list[CoursesTagsResponeModel])
def get_courses(
    skip: int | None = 0,
    take: int |None = 5,
    sorting: str | None = None,
    sort_by: str | None = None,
    search: str | None = None,
    x_token: Optional[str] = Header(None)):

    if not x_token:
        data = list(courses_service.all_non_premium(search, skip, take))    

    else:
        user = get_user_or_raise_401(x_token)
        
        if user.role == Role.ADMIN:
            data = courses_service.all(search, skip, take)

        elif user.role == Role.TEACHER:
            data = courses_service.t_private(user.id, search, skip, take)
        
        else:
            data = courses_service.all_non_hidden(search, skip, take)


    if sorting and (sorting == 'asc' or sorting == 'desc'):
        return courses_service.sorting(data, reverse=sorting == 'desc', attribute=sort_by)
    
    return data


@courses_router.get('/{course_id}', response_model=CourseSectionsResponseModel)
def get_course(course_id:int, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('You need to make registration to view this course!')
    
    user = get_user_or_raise_401(x_token)

    course = courses_service.get_by_id(course_id)

    if course == None:
        return BadRequest(f'Course with {course_id} doesn\'t exist!')
    
    if course.hidden == True and user.role == Role.STUDENT:
        return Unauthorized('You don\'t have permission to view this course')

    return(CourseSectionsResponseModel(course = course, sections = sections_service.get_sections(course_id)))


@courses_router.post('/', response_model=CreateCourse)
def create_courses(course:CreateCourse, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('You are not authorized')

    user = get_user_or_raise_401(x_token)

    if user.role != Role.TEACHER:
        return Forbidden('Only teacher can create course!')
    
    data = teachers_service.check_if_is_approved(user.id)
    if not data:
        return Forbidden('You registration is not approved, yet!')

    course = courses_service.create(course, user.id)

    return course

@courses_router.put('/{course_id}', response_model=Course)
def update_courses(course:Course, course_id:int, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('You are not authorized.')
    
    #if not courses_service.exists(course_id):
    #    return BadRequest(f'Course with {course_id} doesn\'t exist!')
    
    user = get_user_or_raise_401(x_token)

    if user.role == Role.STUDENT:
        return Forbidden('Only teacher or admin can update course!')
    
    old_course = courses_service.get_by_id(course_id)

    if old_course == None:
        return BadRequest(f'Course with id {course_id} doesn\'t exist!')
    
    if user.id != old_course.author_id:
        return Unauthorized('You are not authorized.')
    
    course = courses_service.update(old_course, course)

    return course 


@courses_router.delete('/{course_id}')
def remove_course(course_id:int, x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You are not authorized!')
    
    course = courses_service.get_by_id(course_id)
    if course == None:
        return BadRequest(f'Course with id {course_id} doesn\'t exist!')
    
    user = get_user_or_raise_401(x_token)
    if user.role == Role.STUDENT:
        return Forbidden('You don\'t have permission to delete!')
    
    if user.role == Role.TEACHER and user.id != courses_service.get_course_authorID(course_id):
        return Forbidden('Only the author of this course can delete it!')
    
    progress_service.delete_by_course_id(course_id)
    sections_service.delete_by_course_id(course_id)
    enrollments_service.delete(course_id)
    ratings_service.delete(course_id)
    tags_service.delete(course_id)
    courses_service.delete(course_id)
    
    return Ok(content= f'Course №{course.id} removed!')

@courses_router.get('/avg_rating/{course_id}')
def get_avg(course_id, x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You should have registration!')
    
    return ratings_service.average_rating(course_id)