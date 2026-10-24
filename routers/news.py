from fastapi import APIRouter,Depends,Query,HTTPException
from crud import news
from crud import news_cache
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
#prefix表示前缀，tags表示分组
router=APIRouter(prefix='/api/news',tags=['news'])

#* 分类列表
@router.get('/categories')
async def get_categories(db:AsyncSession=Depends(get_db),skip:int=0,limit:int=100):

    categories=await news_cache.get_categories(db,skip,limit)
    return {
    "code": 200,
    "message": "success",
    "data": categories
    }

#* 新闻列表
@router.get('/list')
async def get_news_list(
    #alias表示真正拼接到url中的参数名称
    category_id:int=Query(...,alias='categoryId'),
    page:int=1,
    page_size:int=Query(10,alias='pageSize',le=100),
    db:AsyncSession=Depends(get_db)
):
    offset=(page-1)*page_size
    news_list=await news_cache.get_news_list(db,category_id,offset,page_size)
    total=await news.get_news_count(db,category_id)

    hasMore=(offset+len(news_list))<total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": hasMore
        }
    }

#* 新闻详情
@router.get('/detail')
async def get_news_detail(
    db:AsyncSession=Depends(get_db),
    news_id:int=Query(...,alias='id')
    ):
    detail=await news.get_news_detail(db,news_id)
    if not detail:
        raise HTTPException(status_code=404,detail='news not found')

    views_res=await news.increase_news_views(db,detail.id)

    related_news=await news.get_related_news(db,detail.category_id,detail.id)
    if not views_res:
        raise HTTPException(status_code=404,detail="news not found")
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": detail.id,
            "title": detail.title,
            "content": detail.content,
            "image": detail.image,
            "author": detail.author,
            "publishTime": detail.publish_time,
            "categoryId": detail.category_id,
            "views": detail.views,
            "relatedNews": related_news
         }
    }   