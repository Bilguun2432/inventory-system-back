from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def successResponse(data: any, message: str|None = None):
    headers = None
    if (message != None):
        headers = {"message": message}
    res = jsonable_encoder(data, exclude={"circular_reference_field"})
    return JSONResponse(content=res, status_code=200, headers=headers)


def createdResponse(data: any, message: str | None = None):
    headers = None
    if (message != None):
        headers = {"message": message}
    res = jsonable_encoder(data)
    return JSONResponse(content=res, status_code=201, headers=headers)


def notFoundResponse(message: str | None):
    msg = message
    if msg == None:
        msg = "Resource not found"            
    headers = {"message": msg}
    res = jsonable_encoder({"message": msg})
    return JSONResponse(content=res, headers=headers, status_code=404)


def badRequestResponse(message: str | None):
    msg = message
    if msg == None:
        msg = "Resource not found"            
    headers = {"message": msg}
    res = jsonable_encoder({"message": msg})
    return JSONResponse(content=res, headers=headers, status_code=400)