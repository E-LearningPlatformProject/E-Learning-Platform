from fastapi import APIRouter, Header
from typing import Optional
from common.responses import NotFound, BadRequest, Ok, Unauthorized, Forbidden
from common.auth import get_user_or_raise_401
from data.models import Role, Section
from services import courses_service, sections_service, progress_service, students_service


section_router = APIRouter(prefix='/sections', tags=['Sections'])

#@section_router.get('/{course_id}')
#def get_sections(course_id:int, x_token: Optional[str] = Header(None)):
#    if not x_token:
#        return Unauthorized('You are not authorized!')
#    
#    user = get_user_or_raise_401(x_token)
#
#    if not courses_service.exists(course_id):
#        return BadRequest(F'Course with ID: {course_id} doesn\'t exist!')
#    
#    if courses_service.is_hidden(course_id) and user.role == Role.STUDENT:
#        return Forbidden('You don\'t have permission to view those sections!')
#    
#    return sections_service.get_sections(course_id)

@section_router.get('/{section_id}', response_model = Section)
def get_section(section_id:int, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('You are not authorized!')
    
    user = get_user_or_raise_401(x_token)

    section = sections_service.get_by_id(section_id)

    if section == None:
        return BadRequest(F'Section with ID: {section_id} doesn\'t exist!')
    
    if user.role == Role.STUDENT:
    
        if courses_service.is_hidden(section.course_id):
            return Forbidden('You don\'t have permission to view those sections!')

        if not students_service.check_if_student_is_enrolled(section.course_id, user.id):
            return Unauthorized('You need to enroll for this course to view this section!')
    
        progress_service.create(user.id, section_id)
    
    return section


@section_router.post('/{course_id}', response_model=Section)
def create_section(section:Section, course_id:int, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('You are not authorized!')

    user = get_user_or_raise_401(x_token)

    if not courses_service.exists(course_id):
        return BadRequest(F'Course with ID: {course_id} doesn\'t exist!')

    if user.role != Role.TEACHER:
        return Forbidden('You don\'t have permission to create section!')
    
    if user.id != courses_service.get_course_authorID(course_id):
        return Forbidden('Only the author of this course can create section!')
    

    section = sections_service.create(section, course_id)

    return section

@section_router.put('/{section_id}', response_model=Section)
def update_section(new_section:Section, section_id:int, x_token: Optional[str] = Header(None)):

    if not x_token:
        return Unauthorized('You are not authorized!')

    user = get_user_or_raise_401(x_token)

    old_section = sections_service.get_by_id(section_id)
    
    if old_section == None:
        return BadRequest(F'Section with ID: {section_id} doesn\'t exist!')

    if user.role != Role.TEACHER:
        return Forbidden('You don\'t have permission to update!')

    if user.id != courses_service.get_course_authorID(old_section.course_id):
        return Forbidden('Only the author of this course can update section!')
    
    section = sections_service.update(old_section, new_section)
    
    return section


@section_router.delete('/{section_id}', response_model=Ok)
def remove_section(section_id:int, x_token: Optional[str] = Header(None)):
    if not x_token:
        return Unauthorized('You are not authorized!')
    
    if not sections_service.exists(section_id):
        return BadRequest(f'Section with id {section_id} doesn\'t exist!')
    
    user = get_user_or_raise_401(x_token)

    section = sections_service.get_by_id(section_id)

    if user.role == Role.STUDENT:
        return Forbidden('You don\'t have permission to delete!')
    
    if user.role == Role.TEACHER and user.id != courses_service.get_course_authorID(section.course_id):
        return Forbidden('Only the author of this course can delete section!')
    
   
    progress_service.delete(section.id)    
    sections_service.delete(section_id)
    
    return Ok(content= f'Section №{section.id} removed!')