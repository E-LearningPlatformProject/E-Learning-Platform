from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, StringConstraints, field_validator
from re import match
from os import getenv


TEmail = Annotated[str, StringConstraints(pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')]

class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'


class User(BaseModel):
    id: int | None
    email:str
    password: str
    
    role:str

    @classmethod
    def from_query_result(cls, id, email, password, role):
        return cls(
            id=id,
            email=email,
            password=password,
            role=role
            )
    
    @field_validator('email')
    def validate_email(cls, email:str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        return email if match(pattern, email) is not None else False

    
    @field_validator('password')
    def validate_password(cls, password:str):
        if len(password) == 64:
            return  password           
            
        pattern = r'^\w{6,30}$'
        
        return password if match(pattern, password) is not None else False
    
class Teachers(BaseModel):
    id:int
    phone_number:int 
    linked_in_account:str 
    is_approved:bool 
    users_id:int
    first_name:str
    last_name:str
    
    @classmethod
    def from_query_result(cls, id, phone_number, linked_in_account, is_approved, users_id, first_name, last_name):
        return cls(
            id=id,
            phone_number=phone_number,
            linked_in_account=linked_in_account,
            is_approved=is_approved,
            users_id=users_id,
            first_name=first_name,
            last_name=last_name
            )
    
class Students(BaseModel):
    id:int
    users_id:int
    first_name:str
    last_name:str

    @classmethod
    def from_query_result(cls, id, users_id, first_name, last_name):
        return cls(
            id=id,
            users_id=users_id,
            first_name=first_name,
            last_name=last_name
        )
    

class LoginData(BaseModel):
    email: TEmail
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

    