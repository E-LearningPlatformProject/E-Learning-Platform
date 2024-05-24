from fastapi import APIRouter, Header
from typing import Optional
from common.responses import NotFound, BadRequest, Unauthorized, Forbidden
from common.auth import get_user_or_raise_401
from data.models import Role, Section
from services import courses_service, sections_service


section_router = APIRouter(prefix='/sections')

#@section_router.get('/{course_id}')
#def get_sections(course_id:int, x_token: Optional[str] = Header(None)):
#    if not x_token:
#        return Unauthorized('You are not authorized')
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

@section_router.get('/{section_id}')
def get_section(section_id:int, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('You are not authorized')
    
    user = get_user_or_raise_401(x_token)

    section = sections_service.get_by_id(section_id)

    if section == None:
        return BadRequest(F'Section with ID: {section_id} doesn\'t exist!')
    
    if courses_service.is_hidden(section.course_id) and user.role == Role.STUDENT:
        return Forbidden('You don\'t have permission to view those sections!')

    if not sections_service.check_if_student_is_enrolled(section.course_id, user.id):
        return Unauthorized('You need to enroll for this course to view this section!')
    
    # Todo - check if progress created, if no create
    
    return section


@section_router.post('/{course_id}')
def create_section(section:Section, course_id:int, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('You are not authorized')

    user = get_user_or_raise_401(x_token)

    if not courses_service.exists(course_id):
        return BadRequest(F'Course with ID: {course_id} doesn\'t exist!')

    if user.role != Role.TEACHER:
        return Forbidden('You don\'t have permission to create section!')
    
    if user.id != courses_service.get_course_authorID(course_id):
        return Forbidden('Only the author of this course can create section!')
    

    section = sections_service.create(section, course_id)

    return section

@section_router.put('/{section_id}')
def update_section(new_section:Section, section_id:int, x_token: Optional[str] = Header(None)):

    if not x_token:
        return Unauthorized('You are not authorized')

    user = get_user_or_raise_401(x_token)

    old_section = sections_service.get_by_id(section_id)
    
    if old_section == None:
        return BadRequest(F'Section with ID: {section_id} doesn\'t exist!')

    if user.role != Role.TEACHER:
        return Forbidden('You don\'t have permission to update!')

    if user.id != courses_service.get_course_authorID(old_section.course_id):
        return Forbidden('Only the author of this course can create section!')
    
    section = sections_service.update(old_section, new_section)
    
    return section

# To do
# @section_router.delete('/{section_id}')