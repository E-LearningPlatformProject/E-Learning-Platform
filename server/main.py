from fastapi import FastAPI

from routers.users import users_router
from routers.courses import courses_router


app = FastAPI()

app.include_router(users_router)
app.include_router(courses_router)

