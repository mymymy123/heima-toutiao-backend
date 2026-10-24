from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Header,Depends,HTTPException,status
from config.db_conf import get_db
import re
from crud import users
#* 根据token查询用户
async def get_current_user(authorization:str=Header(...,alias='Authorization'),db:AsyncSession=Depends(get_db)):
    # token=authorization.split(' ')[1]
    token=authorization.replace('Bearer ','')
    user=await users.get_user_by_token(db,token)
    if not users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户不存在或登录已过期")
    return  user
