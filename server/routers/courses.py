from typing import Optional
from fastapi import APIRouter, Header
from pydantic import BaseModel
from common.responses import BadRequest, Forbidden, NotFound, Unauthorized, Ok
from common.auth import get_user_or_raise_401
