<img src="https://webassets.telerikacademy.com/images/default-source/logos/telerik-academy.svg)" alt="logo" width="300px" style="margin-top: 20px;"/>

# E-Learning Platform

## 1. Project description
Design and implement a E-Learning Platform and provide RESTful API that can be consumed by different students and teachers. High-level description:
- Students can search for and enroll in online courses and view their progress
- Teachers would publish the courses
- Courses can get rating


## 2. API Architecture

-    ![Alt text](MVC.png)

### 1) The folder `data` represent Model
### 2) Controller is split between application layer(`routers`) and business logic(`services`)

## 3. Instructions on how to setup and run the project locally

### 1) You need to have MariaDb server . You can install it from here - https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.3.2

### 2) You can set local virtual environment using your terminal and the commands are:
- For Linux/Mac: 
    - `python3 -m venv .venv`
    - `.venv/bin/activate`
- For Windows: 
    - `py -m venv .venv`
    - `.venv\Scripts\activate`

### 3) The modules that are used for this project can be found in `requirements.txt`. You can install them in your terminal using the command:
- For Linux/Mac: 
    - `python3 -m pip install -r requirements.txt`
- For Windows: 
    - `py -m pip install -r requirements.txt`

### 4) After you have registration for MariaDb you need to put your password so you can run a server. In file `server/data/database.py` in the function called `_get_connection()` on line 10 you can put your password   
- `password = {"YOUR_PASSWORD"}`

As well you need to set a key word that is used to create secure tokens in file `server/data/models.py` on line 152.
- `KEY = {"YOUR_KEY"}`

### 5) You will need google email to set your email verification. You need to visit https://myaccount.google.com/apppasswords. You add app name and automatically password wil be created. Copy the password, open file `server/data/send_mail.py` and add it on line 11 and line 32.
- `password = getenv('APPKEY_eLearning')` 

As well you need to add your google email on lines 10 and 31.
- `username = getenv('EMAIL')`

### 6) When you are ready with the instructions above you need to be in the folder where is the `main.py` file to start your server. You can use the command.
- `uvicorn main:app`

### 7) Once your server is on you can use `Postman` or your browser to check the functionality of the API
- `https://www.postman.com/downloads/`
- `http://127.0.0.1:8000/docs`


## Schema:

-    ![Alt text](schema.png)

## 4. End Points

### `Users`

-  @POST - http://127.0.0.1:8000/users/register/teacher

Body input:
```
{
    "user_data": {
        "id": "1",
        "email": "plamen@abv.bg",
        "password": "123456",
        "role": "teacher"
    },
    "teacher_data": {
        "id": "2",
        "users_id": "5",
        "first_name": "Plamen",
        "last_name": "Plamenov",
        "phone_number": "0885624569",
        "linked_in_account": "P.Plamenov",
        "is_approved": "0",
        "image": "/Users/romario/Telerik Academy/Final Project/E-Learning-Platform/server/data/teacher_images/Dumbledor_Dumbledorov.png"
    }
}
```
Body ouput if body valid:
```
{
    "id": 10,
    "email": "plamen@abv.bg",
    "password": "xxxxxxxxx",
    "role": "teacher"
}
```

Body ouput if email is taken:
```
"Email plamen@abv.bg is taken."
```

-  @POST - http://127.0.0.1:8000/users/login

Body input:
```
{
    "username":"plamen@abv.bg",
    "password":"123456",
}
```
Body ouput if body valid:
```
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTEsInVzZXJuYW1lIjoiSlQiLCJyb2xlIjoidXNlciIsImlhdCI6MTcxNTI3MzMzMCwiZXhwIjoxNzE1MjgwNTMwfQ.Z3bfq2dvtiikv_tvQ1PgvYLmRQoRGd8CSmoq-4jRvoU"
}
```

-  @GET - http://127.0.0.1:8000/users/info

Body ouput if body valid:
```
{
    "id": 10,
    "email": "plamen@abv.bg",
    "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca 020c923adc6c92",
    "role": "teacher"
}
```

### `Courses`
-  @POST- http://127.0.0.1:8000/courses/

Body input:
```
    {
        "id": 1,
        "title": "Python for begginers",
        "description": "Foundamental skills working with Python",
        "level": "public",
	    "image": "URL_DRIVE_LOCATION",
        "tags": "Python,Math"
    }
```

Body ouput if body valid:
```
{
    "id": 6,
    "title": "Python for begginers",
    "description": "Foundamental skills working with Python",
    "level": "public",
    "tags": "Python,Math"
}
```

-  @GET - http://127.0.0.1:8000/courses/

Body ouput if token is valid:
```
[
    {
        "id": 1,
        "title": "Python for begginers",
        "description": "Foundamental skills working with Python",
        "level": "public",
        "image": "https://telerikacademy-my.sharepoint.com/:i:/r/personal/romario_dimitrov_a57_learn_telerikacademy_com/Documents/Images/Python.svg.png?csf=1&web=1&e=v6H6cJ",
        "tags": "Python,Math"
    },
    {
        "id": 2,
        "title": "Building Databases",
        "description": "Build database from zero to hero",
        "level": "premium",
        "image": "https://telerikacademy-my.sharepoint.com/:i:/r/personal/romario_dimitrov_a57_learn_telerikacademy_com/Documents/Images/database.png?csf=1&web=1&e=XvZ8WQ",
        "tags": "Python"
    },
    {
        "id": 4,
        "title": "C++ for begginers",
        "description": "Foundamental skills working with C++",
        "level": "public",
        "image": "https://telerikacademy-my.sharepoint.com/:i:/r/personal/romario_dimitrov_a57_learn_telerikacademy_com/Documents/Images/c++.jpg?csf=1&web=1&e=kCc1c5",
        "tags": "C++"
    }
]
```

-  @GET - http://127.0.0.1:8000/courses/{course_id}

Body ouput if token is valid:
```
{
    "course": {
        "id": 1,
        "title": "Python for begginers",
        "description": "Foundamental skills working with Python",
        "level": "public",
        "hidden": false,
        "image": "https://telerikacademy-my.sharepoint.com/:i:/r/personal/romario_dimitrov_a57_learn_telerikacademy_com/Documents/Images/Python.svg.png?csf=1&web=1&e=v6H6cJ",
        "author_id": 1,
        "tags": "Python,Math"
    },
    "sections": [
        {
            "id": 1,
            "title": "IF Statement",
            "type_file": "txt",
            "course_id": 1,
            "source": "URL"
        },
        {
            "id": 2,
            "title": "Multiple statements",
            "type_file": "txt",
            "course_id": 1,
            "source": "URL"
        },
        {
            "id": 3,
            "title": "For loop",
            "type_file": "doc",
            "course_id": 1,
            "source": "URL"
        }
    ]
}
```
Body ouput if there is no token:
```
"You need to make registration to view this course!"
```


### `Students`

-  @POST- http://127.0.0.1:8000/students/enrolment/{course_id}'

Body ouput if token valid:
```
"Student's enrollment requested!"
```

-  @GET- http://127.0.0.1:8000/students/progress/{course_id}

Body ouput if token valid:
```
'Your progress is 67% for Course with ID: 1'
```

-  @POST- http://127.0.0.1:8000/students/rating
Body input:
```
{
    "course_id":1,
    "rating":8
}
```

Body ouput if body valid:
```
Your vote was seccesfull!
```
Body ouput if body is not valid:
```
'Your vote must be betweeen 1 and 10'
```


-  @GET- http://127.0.0.1:8000/categories/{id}

Body ouput if body valid:
```
{
    "category": {
        "id": 3,
        "name": "Bear88",
        "is_private": 1,
        "is_locked": 0
    },
    "topics": [
        {
            "id": 1,
            "title": "Meeting",
            "content": "Tomorrow we have meeting at 8:00 o'clock.",
            "best_reply_id": 0,
            "locked": false,
            "categories_id": 3,
            "author_id": 4
        }
    ]
}
```
-  @PUT- http://127.0.0.1:8000/students

Body input:
```
{
  "id": 4,
  "email": "daniel34@abc.com",
  "password": "123de5a",
  "role": "student",
  "first_name": "Daniel",
  "last_name": "Angelov"
}
```

### `Sections`

- @GET - http://127.0.0.1:8000/sections/{section_id}

Body ouput:
```
{
    "id": 1,
    "title": "IF Statement",
    "type_file": "txt",
    "course_id": 1,
    "source": "URL"
}
```

- @POST - http://127.0.0.1:8000/sections/{course_id}

Body input:
```
{
    "id": 2,
    "title": "Loops",
    "type_file": "txt",
    "course_id": 1,
    "source": "URL"
}
```

Body ouput if token valid:
```
{
    "id": 9,
    "title": "Loops",
    "type_file": "txt",
    "course_id": 1,
    "source": "URL"
}
```
Body ouput if the author is not the one created the course:
```
'Only the author of this course can create section!'
```
- @POST - http://127.0.0.1:8000/permissions/all

Body input:
```
{
    "category_id":3,
    "user_id":2,
    "write_permission":0
}
```

```
Read permission created!
```

- @DELETE - http://127.0.0.1:8000/sections/{section_id}

Body ouput if section exist:
```
Section № 9 removed!
```