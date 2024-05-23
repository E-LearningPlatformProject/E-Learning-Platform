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
    
class StudentInfo(BaseModel):
    id: int
    email: str
    password: str
    role: str
    first_name: str
    last_name: str

    @classmethod
    def from_query_result(cls, id, email, password, role, first_name, last_name):
        return cls(
            id=id,
            email=email,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name
        )

class TeacherInfo(BaseModel):
    id: int
    email: str
    password: str
    role: str
    first_name: str
    last_name: str
    phone_number: int
    linked_in_account: str
    is_approved: bool

    @classmethod
    def from_query_result(cls, id, 
                        email,
                        password, 
                        role, 
                        first_name, 
                        last_name, 
                        phone_number,
                        linked_in_account,
                        is_approved):
        
        return cls(
            id=id,
            email=email,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            linked_in_account=linked_in_account,
            is_approved=is_approved
        )



class LoginData(BaseModel):
    email: TEmail
    password: str

class Key:
    KEY = getenv('KEY')

class Tag(BaseModel):
    #id:int
    title:str

    @classmethod
    def from_query_result(cls, title):
        return cls(
       
            title = title)


class CoursesTagsResponeModel(BaseModel):
    id:int
    title: str
    description: str
    level:str
    tags: str | None

    @classmethod
    def from_query_result(cls, id, title, description,level, tags):
        return cls(
            id = id,
            title = title,
            description = description,
            level = level,
            tags = tags)


class CreateCourse(BaseModel):
    id:int
    title: str
    description: str
    level:str
    tags: str | None

    @classmethod
    def from_query_result(cls, id, title, description,level, tags):
        return cls(
            id = id,
            title = title,
            description = description,
            level = level,
            tags = tags)

class Course(BaseModel):
    id:int
    title: str
    description: str
    level:str
    hidden:bool
    author_id: int
    tags: str | None

    @classmethod
    def from_query_result(cls, id, title, description, level, hidden, author_id, tags):
        return cls(
            id=id,
            title = title,
            description = description,
            level = level,
            hidden = hidden,
            author_id = author_id,
            tags = tags)