from models.history import History
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete,func
from models.news import News


#* 添加历史记录
async def add_history(
        db:AsyncSession,
        user_id:int,
        news_id:int
):
    query=select(History).where(History.news_id==news_id)
    result=await db.execute(query)
    history=result.scalar_one_or_none()
    if history:
        history.view_time=func.now()
    else:
        history=History(
                user_id=user_id,
                news_id=news_id
            )
        db.add(history)
    await db.commit()
    await db.refresh(history)
    return history

#* 获取历史记录
async def get_history(
        db:AsyncSession,
        user_id:int,
        page:int,
        page_size:int
):
    offset=(page-1)*page_size
    query=select(News,History.id.label('history_id'),History.view_time).join(History,History.news_id==News.id).where(
        History.user_id==user_id
    ).offset(offset).limit(page_size).order_by(History.view_time.desc())

    result=await db.execute(query)
    rows=result.all()

    query=select(func.count()).where(History.user_id==user_id)
    count_result=await db.execute(query)
    total=count_result.scalar_one()
    return rows,total

#* 删除历史记录
async def delete_history(
        db:AsyncSession,
        user_id:int,
        news_id:int
):
    query=delete(History).where(History.news_id==news_id,History.user_id==user_id)
    result=await db.execute(query)
    await db.commit()
    return result.rowcount>0


#* 清空历史记录
async def clear_history(db:AsyncSession,user_id:int):
    query=delete(History).where(History.user_id==user_id)
    result=await db.execute(query)
    await db.commit()
    return result.rowcount