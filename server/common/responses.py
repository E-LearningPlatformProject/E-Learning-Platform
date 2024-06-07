from starlette.responses import JSONResponse


class BadRequest(JSONResponse):
    def __init__(self, content=''):
        super().__init__(status_code=400, content=content)


class NotFound(JSONResponse):
    def __init__(self, content=''):
        super().__init__(status_code=404, content=content)


class Unauthorized(JSONResponse):
    def __init__(self, content=''):
        super().__init__(status_code=401, content=content)

class Forbidden(JSONResponse):
    def __init__(self, content=''):
        super().__init__(status_code=403, content=content)


class NoContent(JSONResponse):
    def __init__(self):
        super().__init__(status_code=204)

class Ok(JSONResponse):
    def __init__(self, content=''):
        super().__init__(status_code=200, content=content)