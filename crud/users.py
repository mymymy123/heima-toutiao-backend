from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,delete
from models.users import User,UserToken
from schemas.users import UserRequast,UserUpdateRequest
from utils import security
from datetime import datetime,timedelta
import uuid
from fastapi import HTTPException,status
#* 根据用户名查询用户
async def get_user_by_username(db:AsyncSession,username:str):
    query=select(User).where(User.username==username)
    result=await db.execute(query)
    return result.scalar_one_or_none()

#* 创建用户
async def create_user(db:AsyncSession,user_data:UserRequast):
    hashed_password=security.get_hash_password(user_data.password)
    user=User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) #从数据库返回最新user
    return user


#* 生成token
async def create_token(db:AsyncSession,user_id:int):
    token=str(uuid.uuid4())
    expires_at=datetime.now() + timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
    await db.commit()
    return token


#* 用户登录
async def authenticate_user(db:AsyncSession,username:str,password:str):
    existing_user=await get_user_by_username(db,username)
    if not existing_user:
        return None
    if not security.verify_password(password,existing_user.password):
        return None
    return existing_user


#* 获取用户信息
#todo 验证token -》 查询用户
async def get_user_by_token(db:AsyncSession,token:str):
    query=select(UserToken).where(UserToken.token==token)
    result=await db.execute(query)
    db_token=result.scalar_one_or_none()

    if not db_token or db_token.expires_at< datetime.now():
        return None

    query=select(User).where(User.id==db_token.user_id)
    result=await db.execute(query)
    return result.scalar_one_or_none()
    

#* 更新用户信息
async def update_user(db:AsyncSession,username:str,user_data:UserUpdateRequest):
    #model_dump 将pydantic模型转换为字典
    stmt=update(User).where(User.username==username).values(**user_data.model_dump(
        exclude_unset=True, ##设置值的才会被提取
        exclude_none=True
    ))
    result=await db.execute(stmt)
    await db.commit()
    if result.rowcount==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户不存在")
    updated_user= await get_user_by_username(db,username)
    return  updated_user

#*修改密码
async def change_password(db:AsyncSession,user:User,old_password:str,new_password:str):
    if not security.verify_password(old_password,user.password):
        return False
    hashed_new_pwd=security.get_hash_password(new_password)
    # stmt=update(User).where(User.id==user.id).values(password=hashed_new_pwd)
    # db.execute(stmt)
    user.password=hashed_new_pwd
    #防止数据库会话过期或关闭导致的不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True