from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.sql.functions import user
from starlette.routing import Router
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine

from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest
from config.db_conf import get_db
from crud import users
from utils.auth import get_current_user
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
# 查Token查用户->封装crud->功能整合成一个工具函数->路由导入使用：依赖注入
@router.get("/info")
async def get_user_info(user:User = Depends(get_current_user)):
    return success_response(message='获取用户信息成功',data=UserInfoResponse.model_validate(user))

# 修改用户信息：验证Token->更新(用户输入数据 put提交->请求体参数->定义pydantic模型类)->响应结果
# 参数：用户输入的+验证Token的+db(调用更新的方法)
@router.put("/update")
async def update_user_info(user_data:UserUpdateRequest,db:AsyncSession=Depends(get_db),user:User = Depends(get_current_user)):
    user=await users.update_user(db,user.username,user_data)
    return success_response(message='更新用户信息成功',data=UserInfoResponse.model_validate(user))




















