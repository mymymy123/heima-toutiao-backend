from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,update,and_
from models.news import Category,News
from cache.news_cache import *
from fastapi.encoders import jsonable_encoder
from schemas.base import NewsItemBase
#* 得到分类列表
async def get_categories(db:AsyncSession,skip:int=0,limit:int=100):
    #尝试从缓存中获取
    cached_categories=await get_cache_categories()
    if cached_categories:
        
        return cached_categories
    
    result=await db.execute(select(Category)
                      .offset(skip)
                      .limit(limit))
    categories=result.scalars().all()

    #写入缓存
    if categories:
        categories=jsonable_encoder(categories)
        await set_cache_categories(categories)
        print('存储成功')

    return categories

#* 新闻列表
async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    #todo 查询指定分类下的所有新闻
    page=skip/limit+1
    cache_news_list=await get_cache_news_list(category_id,page,limit)
    if cache_news_list:
        return [News(**item) for item in cache_news_list]

    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    news_list=result.scalars().all()

    if news_list:
        #把orm对象转换为字典
        news_data=[NewsItemBase.model_validate(item).model_dump(mode='json',by_alias=False) for item in news_list]
        await set_cache_news_list(category_id,page,limit,news_data)

    return news_list

#* 数据总量
async def get_news_count(db:AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)
    return result.scalar_one()


#* 新闻详情
async def get_news_detail(db:AsyncSession,news_id:int):
    stmt=select(News).where(News.id==news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()

#* 增加浏览量

async def increase_news_views(db:AsyncSession,news_id:int):
    stmt=update(News).where(News.id==news_id).values(views=News.views+1)
    result=await db.execute(stmt)
    await db.commit()
    #检查是否命中数据
    return result.rowcount>0


#* 查询相关新闻
async def get_related_news(db:AsyncSession,category_id:int,news_id:int,limit:int=5):
    stmt=select(News).where(and_(News.category_id==category_id,News.id !=news_id)).order_by(News.views.desc(),News.publish_time.desc()).limit(limit)
    result=await db.execute(stmt)
    await db.commit()
    related_news= result.scalars().all()
    return [{
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time,
        "categoryId": news.category_id,
        "views": news.views,
    } for news in related_news]

