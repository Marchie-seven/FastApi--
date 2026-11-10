from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.sql.functions import user
from starlette.routing import Router
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from config.db_conf import get_db
from crud import users
from utils.response import success_response

router=APIRouter(prefix="/api/users",tags=["users"])

#用户注册
@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):#用户信息和db
    #注册逻辑：验证用户是否存在->创建用户->生成Token ->响应结果
    existing_user=await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400,detail="用户已存在")
    user=await users.create_user(db,user_data)
    token=await users.create_token(db,user.id)
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message='注册成功',data=response_data)

#用户登录
@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    #登录逻辑：验证用户是否存在->验证密码->生成Token ->响应结果
    user=await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=401,detail="用户名或密码错误")
    token=await users.create_token(db,user.id)
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message='登录成功',data=response_data)

#获取用户信息
# 查Token查用户->封装crud->功能整合成一个工具函数->路由导入使用
@router.get("/info")
async def get_user_info():
    return success_response(message='获取用户信息成功')





















