from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, StringConstraints, field_validator, Field
from re import match
from os import getenv
from pathlib import Path
from fastapi.responses import FileResponse


TEmail = Annotated[str, StringConstraints(pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')]

class AdminEmail:
    _EMAIL = 'admin@admin.com'

class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'


class User(BaseModel):
    id: int | None = Field(examples=[8])
    email:str = Field(examples=["ivan0198@abv.bg"])
    password: str = Field(examples=["123456"])
    role:str = Field(examples=["teacher / student"])

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
    id:int = Field(examples=["3"])
    phone_number:int = Field(examples=["003598977658765"])
    linked_in_account:str = Field(examples=["https://www.linkedin.com/in/ivanivanov"])
    is_approved:bool = Field(examples=[True])
    users_id:int = Field(examples=["8"])
    first_name:str = Field(examples=["Ivan"])
    last_name:str = Field(examples=["Ivanov"])
    image: str = Field(examples=["PATH/image.png"])
    
    @classmethod
    def from_query_result(cls, id, phone_number, linked_in_account, is_approved, users_id, first_name, last_name, image):
        return cls(
            id=id,
            phone_number=phone_number,
            linked_in_account=linked_in_account,
            is_approved=is_approved,
            users_id=users_id,
            first_name=first_name,
            last_name=last_name,
            image=image
            )
    
class Students(BaseModel):
    id:int = Field(examples=["4"])
    users_id:int = Field(examples=["9"])
    first_name:str = Field(examples=["Daniel"])
    last_name:str = Field(examples=["Angelov"])

    @classmethod
    def from_query_result(cls, id, users_id, first_name, last_name):
        return cls(
            id=id,
            users_id=users_id,
            first_name=first_name,
            last_name=last_name
        )
    
class StudentInfo(BaseModel):
    id: int = Field(examples=["4"])
    email: str = Field(examples=["daniel34@abc.com"])
    password: str = Field(examples=["123de5a"])
    role: str = Field(examples=["student"])
    first_name: str = Field(examples=["Daniel"])
    last_name: str = Field(examples=["Angelov"])

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
    id: int = Field(examples=["6"])
    email: str = Field(examples=["name@abc.com"])
    password: str = Field(examples=["na12345"])
    role: str = Field(examples=["teacher"])
    first_name: str = Field(examples=["Angel"])
    last_name: str = Field(examples=["Ivanov"])
    phone_number: int = Field(examples=["00545356355"])
    linked_in_account: str = Field(examples=["https://www.linkedin.com/in/ivanov"])
    is_approved: bool = Field(examples=[True])
    image : str = Field(examples=["PATH/image.png"])

    @classmethod
    def from_query_result(cls, id, 
                        email,
                        password, 
                        role, 
                        first_name, 
                        last_name, 
                        phone_number,
                        linked_in_account,
                        is_approved,
                        image):
        
        return cls(
            id=id,
            email=email,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            linked_in_account=linked_in_account,
            is_approved=is_approved,
            image=image)



class LoginData(BaseModel):
    email: TEmail = Field(examples=["name@abc.com"])
    password: str = Field(examples=["123456"])

class Key:
    KEY = getenv('KEY')

class Tag(BaseModel):
    #id:int
    title:str = Field(examples=["Math"])

    @classmethod
    def from_query_result(cls, title):
        return cls(
       
            title = title)


class CoursesTagsResponeModel(BaseModel):
    id:int = Field(examples=["6"])
    title: str = Field(examples=["Programming for begginers"])
    description: str = Field(examples=["Basic knowledge for programming"])
    level: str = Field(examples=["public / premium"])
    image: str = Field(examples=["URL"])
    tags: str | None = Field(examples=["Math, Programming"])

    @classmethod
    def from_query_result(cls, id, title, description,level, image,tags):
        return cls(
            id = id,
            title = title,
            description = description,
            level = level,
            image = image,
            tags = tags)


class CreateCourse(BaseModel):
    id:int = Field(examples=["2"])
    title: str = Field(examples=["Programming for begginers"])
    description: str = Field(examples=["Basic knowledge for programming"])
    level:str = Field(examples=["public / premium"])
    tags: str | None = Field(default=None,examples=["Math, Programming"])

    @classmethod
    def from_query_result(cls, id, title, description,level, tags):
        return cls(
            id = id,
            title = title,
            description = description,
            level = level,
            tags = tags)

class Course(BaseModel):
    id:int = Field(examples=["2"])
    title: str = Field(examples=["Programming for begginers"])
    description: str = Field(examples=["Basic knowledge for programming"])
    level:str = Field(examples=["public / premium"])
    hidden:bool = Field(examples=[True])
    image:str = Field(examples=["URL"])
    author_id: int = Field(examples=["1"])
    tags: str | None = Field(default=None,examples=["Math, Programming"])

    @classmethod
    def from_query_result(cls, id, title, description, level, hidden, image, author_id, tags):
        return cls(
            id=id,
            title = title,
            description = description,
            level = level,
            hidden = hidden,
            image = image,
            author_id = author_id,
            tags = tags)
    
class Section(BaseModel):
    id:int = Field(examples=["1"])
    title:str = Field(examples=["Loops"]) 
    type_file:str = Field(examples=["doc"])
    course_id:int = Field(examples=["3"])
    source:str = Field(examples=["URL"])

    @classmethod
    def from_query_result(cls, id, title, type_file, course_id, source):
        return cls(
            id=id,
            title = title,
            type_file = type_file,
            course_id = course_id,
            source = source)
    
class CourseSectionsResponseModel(BaseModel):
    course: Course  = Field(examples=["Course"])
    sections: list[Section]  = Field(examples=["doc"])

      
class Enrollments(BaseModel):
    course_id: int = Field(examples=["4"])
    student_id: int = Field(examples=["2"])

    @classmethod
    def from_query_result(cls, course_id, student_id):
        return cls(
            course_id = course_id,
            student_id = student_id)
    
class Vote(BaseModel):
    course_id:int = Field(examples=["2"])
    rating:int = Field(examples=["8"])

    @field_validator('rating')
    def validate_email(cls, rating:str):
        pattern = r'([1-9]|10)$'
        
        return rating if match(pattern, str(rating)) is not None else False
            

class PremiumCourseCount(BaseModel):
    premium_course_count: int = Field(examples=["5"])

class Route:
    ROUTE_TEACH_IMAGES = '/Users/romario/Telerik Academy/Final Project/E-Learning-Platform/server/data/teacher_images/'
