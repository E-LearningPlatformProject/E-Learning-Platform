from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, StringConstraints, field_validator
from re import match
from os import getenv

class Role:
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'

TUsername = Annotated[str, StringConstraints(pattern=r'^\w{2,30}$')]
TEmail = Annotated[str, StringConstraints(pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')]

class User(BaseModel):
    id: int | None
    username: str
    password: str
    role: str
    email:str

    def is_admin(self):
        return self.role == Role.ADMIN

    @classmethod
    def from_query_result(cls, id, username, password, role, email):
        return cls(
            id=id,
            username=username,
            password=password,
            role=role,
            email=email)
    
    @field_validator('username')
    def validate_username(cls, username:str):
        pattern = r'^\w{2,30}$'
        
        return username if match(pattern, username) is not None else False

    
    @field_validator('password')
    def validate_password(cls, password:str):
        if len(password) == 64:
            return  password           
            
        pattern = r'^\w{6,30}$'
        
        return password if match(pattern, password) is not None else False
    
    @field_validator('email')
    def validate_email(cls, email:str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        return email if match(pattern, email) is not None else False


class LoginData(BaseModel):
    username: TUsername
    password: str

class Key:
    KEY = getenv('KEY')

class Tag(BaseModel):
    id:int
    title:str

    @classmethod
    def from_query_result(cls, id, title):
        return cls(
            id = id,
            title = title)

class Course_UnAutUser(BaseModel):
    id:int
    title: str
    description: str
    

    @classmethod
    def from_query_result(cls, id, title, description):
        return cls(
            id = id,
            title = title,
            description = description
            )


class CourseResponseModel_UnAutUser(BaseModel):
    course: Course_UnAutUser
    tags: list[Tag]
    

    @classmethod
    def from_query_result(cls, course,tag):
        return cls(
            course = course,
            tag = tag
            )

class CourseResponseModel_StUser(BaseModel):
    id:int
    title: str
    description: str
    level: str
    author_id:int

    @classmethod
    def from_query_result(cls, id, title, description, level, author_id):
        return cls(
            id = id,
            title = title,
            description = description,
            level = level,
            author_id = author_id
            )
    
class CourseResponseModel_TchUser(BaseModel):
    id:int
    title: str
    description: str
    level: str

    @classmethod
    def from_query_result(cls, id, title, description, level):
        return cls(
            id = id,
            title = title,
            description = description,
            level = level
            )

class CreateCourse(BaseModel):
    title: str
    description: str
    level: str
    tags: list[Tag]

    