from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,update,and_
from models.news import Category,News

#* 得到分类列表
async def get_categories(db:AsyncSession,skip:int=0,limit:int=100):
    result=await db.execute(select(Category)
                      .offset(skip)
                      .limit(limit))
    categories=result.scalars().all()
    return categories

#* 新闻列表
async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    #todo 查询指定分类下的所有新闻

    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()

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

