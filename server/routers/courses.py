from typing import Optional
from fastapi import APIRouter, Header
from pydantic import BaseModel
from common.responses import BadRequest, Forbidden, NotFound, Unauthorized, Ok
from common.auth import get_user_or_raise_401
from services import courses_service, tags_service
from data.models import Role, CreateCourse



courses_router = APIRouter(prefix='/courses')

@courses_router.get('/')
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
            data = courses_service.t_private(search, user.id, skip, take)
        
        else:
            data = courses_service.all_non_hidden(search, skip, take)


    if sorting and (sorting == 'asc' or sorting == 'desc'):
        return courses_service.sorting(data, reverse=sorting == 'desc', attribute=sort_by)
    
    return data


@courses_router.post('/')
def create_courses(course:CreateCourse, x_token: Optional[str] = Header(None)):
    
    if not x_token:
        return Unauthorized('Go home')

    user = get_user_or_raise_401(x_token)
    
    course = courses_service.create(course, user.id)

    return course
    