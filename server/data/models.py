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