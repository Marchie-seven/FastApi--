from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, \
    general_exception_handler


def register_exception_handlers(app):
    """
    注册异常处理函数:子类在前父类在后：具体的在前不具体的在后
    """
    app.add_exception_handler(HTTPException, http_exception_handler)#业务
    app.add_exception_handler(IntegrityError,integrity_error_handler)#数据库完整性错误
    app.add_exception_handler(SQLAlchemyError,sqlalchemy_error_handler)#数据库错误
    app.add_exception_handler(Exception,general_exception_handler)#一般异常






