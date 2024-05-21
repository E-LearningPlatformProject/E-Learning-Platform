from fastapi import FastAPI

from routers.users import users_router
from routers.students import students_router
from routers.teachers import teachers_router

app = FastAPI()

app.include_router(users_router)
app.include_router(students_router)
app.include_router(teachers_router)



#{
#    "user_data": {
#        "id": 7,
#        "email": "petio@abv.bg",
#        "password": "xxxxxxxxx",
#        "role": "student"
#    },
#    "student_data": {
#        "id": 4,
#        "users_id": 7,
#        "first_name": "Petio",
#        "last_name": "Petrov"
#    }
#}


#{
#    "user_data": {
#        "id": "1",
#        "email": "plamen@abv.bg",
#        "password": "123456",
#        "role": "teacher"
#    },
#    "teacher_data": {
#        "id": "2",
#        "users_id": "5",
#        "first_name": "Plamen",
#        "last_name": "Plamenov",
#        "phone_number": "0885624569",
#        "linked_in_account": "P.Plamenov",
#        "is_approved": "0"
#    }
#}