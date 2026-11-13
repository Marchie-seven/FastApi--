from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo, Field


class UserRequest(BaseModel):
    username: str
    password: str
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="用户昵称")
    avatar: Optional[str] = Field("https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg", max_length=255, description="用户头像")
    gender: Optional[str] = Field("unknown", description="用户性别")
    bio: Optional[str] = Field("这个人很懒什么都没有留下", max_length=500, description="用户简介")
#userinfo对应的类：基础类+info类（id、用户名）
class UserInfoResponse(UserInfoBase):
   id:int
   username: str
   model_config = ConfigDict(
       from_attributes=True,  # 允许从orm对象中取值
   )

# data数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse=Field(...,alias="userInfo")
    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True,#alias/字段名兼容
        from_attributes=True,#允许从orm对象中取值
    )
#更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: str=None
    avatar: str=None
    gender: str=None
    bio: str=None
    phone: str=None
#修改用户密码
class UserChangeRequest(BaseModel):
    old_password: str=Field(...,description="旧密码",alias="oldPassword")
    new_password: str=Field(...,description="新密码",min_length=6,alias="newPassword")











