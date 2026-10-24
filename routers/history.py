from fastapi import APIRouter,Depends,HTTPException,status,Query
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.history import *
from utils.auth import get_current_user
from models.users import User
from crud import history
from utils.response import success_response
router=APIRouter(prefix='/api/history',tags=['histroy'])





@router.post('/add')
async def add_history(
    data:HistoryAddRequest,
    user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    # is_added=await history.check_history(db,data.news_id)
    # if is_added:
    #     return  success_response(
    #             message='添加历史成功',
    #             data=result
    #         )
    result=await history.add_history(db,user.id,data.news_id)
    return success_response(
        message='添加历史成功',
        data=result
    )

@router.get('/list')
async def get_history_list(
    page:int=1,
    page_size:int=Query(100,alias='pageSize'),
    user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
    ):
    rows,total=await history.get_history(db,user.id,page,page_size)
    history_list=[
        {
            **news.__dict__,
            'historyId':history_id,
            'viewTime':view_time
        } for news,history_id,view_time in rows
    ]
    has_more=total>page*page_size
    data=HistoryListResponse(
        list=history_list,
        total=total,
        hasMore=has_more
    )
    return success_response(
        message='获取浏览记录成功',
        data=data
    )

@router.delete('/delete/{news_id}')
async def delte_history(news_id:int,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    is_deleted=await history.delete_history(db,user.id,news_id)
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='该记录不存在')
    return success_response(
        message='删除成功'
    )

@router.delete('/clear')
async def clear_history(user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    delet_count=await history.clear_history(db,user.id)
    return success_response(
        message=f'浏览历史清空成功,共清除{delet_count}条'
    )