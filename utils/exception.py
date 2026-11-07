
import traceback
from fastapi import HTTPException,Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from starlette import status
# 开发阶段（教学/本地调试）：必须设为 True
# 生产环境（上线服务器）：必须设为 False
# 作用：控制是否返回详细错误堆栈、敏感信息

DEBUG_MODE = True
# DEBUG_MODE = True  # 教学项目保持开启
# http_exception_handler：处理主动抛出的业务异常（如参数错误、未登录）
# integrity_error_handler：处理数据库约束错误（用户名重复、外键错误）
# sqlalchemy_error_handler：处理数据库通用错误（连接失败、查询失败）
# general_exception_handler：兜底处理所有未知错误（防止程序崩溃）
# ===================== 异常处理函数 =====================
async def http_exception_handler(request:Request,exc:HTTPException):
    """
    处理 FastAPI 主动抛出的 HTTPException 异常
    这类异常通常是业务代码主动抛出的（如参数错误、权限不足、资源不存在）
    """
    # 处理HHTTPException异常
    # 通常是业务逻辑主动抛出的
    # 返回统一格式的JSON响应
    return JSONResponse(
        # 状态码使用异常本身定义的状态码（如400、401、404）
        status_code=exc.status_code,
        content={
            # 统一响应结构：code=状态码，message=错误信息，data=异常数据（这里无数据）
            'code':exc.status_code,
            'message':exc.detail,
            'data':None
        }
    )

async def integrity_error_handler(request:Request,exc:IntegrityError):
    """
    处理数据库完整性约束错误（IntegrityError）
    常见场景：用户名重复、手机号重复、外键关联数据不存在
    """
    # 处理数据库完整性约束错误
    # 获取数据库原始错误信息（字符串格式）
    error_msg=str(exc.orig)
    # 判断具体的约束错误类型
    # 根据原始错误信息，判断具体是哪种约束错误，返回友好提示
    if "username_UNION" in error_msg or "Duplicate entry" in error_msg:
        # 唯一键重复（如用户名已被注册）
        detail="用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        # 外键约束失败（关联数据不存在）
        detail="关联数据不存在"
    else:
        # 其他数据库约束错误
        detail="数据约束冲突，请检查输入"
    # 开发模式下返回详细错误信息
    # 定义错误详情数据，默认空
    error_data=None
    if DEBUG_MODE:
        # 开发模式下：返回详细错误信息（方便调试）
        error_data={
            "error_type":"IntegrityError",# 异常类型
            "error_detail":error_msg,# 原始错误信息
            "path":str(request.url) # 出错的接口路径
        }
        # 返回400客户端错误响应
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code":400,
            "message":detail,
            "data":error_data# 开发模式有详情，生产模式为空
        }
    )

async def sqlalchemy_error_handler(request:Request,exc:SQLAlchemyError):
    # 处理salalchemy数据库错误
    """
    处理通用数据库操作异常（SQLAlchemyError）
    如：数据库连接失败、SQL语法错误、查询超时等
    这类属于服务器端错误，返回500
    """
    error_data=None
    if DEBUG_MODE:
        # 开发模式：返回完整异常信息 + 堆栈 + 路径
        error_data={
            "error_type":type(exc).__name__,# 异常类名
            "error_detail":str(exc), # 异常描述
            # 格式化异常信息为字符串，方便日志记录和调试
            "traceback":traceback.format_exc(), # 完整堆栈（关键：定位代码行）
            "path":str(request.url)# 请求路径
        }
        # 返回500服务器内部错误
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":500,
            "message":"数据库操作失败，请稍后重试",
            "data":error_data
        }
    )


async def general_exception_handler(request:Request,exc:Exception):
    # 处理所有未捕获的异常
    """
    全局兜底异常处理
    捕获所有**未被上面任何一个异常处理函数捕获**的错误
    确保程序不会崩溃，且前端永远能收到规范响应
    """
    error_data=None
    if DEBUG_MODE:
        error_data={
            "error_type":type(exc).__name__,# 异常类型
            "error_detail":str(exc),# 异常信息
            #格式化异常信息为字符串，方便日志记录和调试
            "traceback":traceback.format_exc(),# 完整堆栈
            "path":str(request.url)# 出错接口
        }
    # 返回500通用服务器错误
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":500,
            "message":"服务器内部错误",
            "data":error_data
        }
    )