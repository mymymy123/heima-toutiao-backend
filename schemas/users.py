from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
class UserRequast(BaseModel):
    username:str
    password:str


class UserInfoBase(BaseModel):
    """
    ⽤户信息基础数据模型
        """

    nickname: Optional[str] = Field(None,max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")

class UserInfoResponse(UserInfoBase):
    id:int
    username:str

    model_config=ConfigDict(
        from_attributes=True
    )

class UserAuthResponse(BaseModel):
    token:str
    user_info:UserInfoResponse=Field(...,alias='userInfo')

    #模型类配置
    model_config=ConfigDict(
        populate_by_name=True, #字段名和 alias 都能用，避免"只能传驼峰、Python 里构造麻烦"
        from_attributes=True #能从 ORM 对象/任意对象属性读取，而不只限于 dict
    ) 


#* 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname:str=None
    avatar:str=None
    gender:str=None
    bio:str=None
    phone:str=None


class UserChangePasswordRequest(BaseModel):
    old_password:str=Field(...,alias='oldPassword')
    new_password:str=Field(...,min_length=6,alias='newPassword')
