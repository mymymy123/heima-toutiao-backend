from fastapi import FastAPI
from utils.exception import *
from fastapi import HTTPException, Request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def register_exception_handlers(app:FastAPI):

    #* 注册全局异常处理函数:子类在前，父类在后，具体的在前面，抽象的在后面
    app.add_exception_handler(HTTPException,http_exception_handler)

    app.add_exception_handler(IntegrityError,integrity_error_handler)

    app.add_exception_handler(SQLAlchemyError,sqlalchemy_error_handler)

    app.add_exception_handler(Exception,general_exception_handler)