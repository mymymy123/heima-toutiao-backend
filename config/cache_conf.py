import redis.asyncio as redis
from redis.asyncio import ConnectionPool
from typing import Any
import json
from environs import Env

env=Env()
env.read_env()


redis_url=env.str("REDIS_URL")
pool=ConnectionPool.from_url(url=redis_url)
redis_client=redis.Redis(
    connection_pool=pool,
    decode_responses=True #是否将字节数据解码为字符串
    )

#* 设置和读取缓存

#字符串
async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f'获取缓存失败:{e}')
        return None

#列表或字典
async def get_json_cache(key:str):
    try:
        data= await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f'获取json缓存失败:{e}')
        return None

#设置缓存 ,过期时间单位为秒
async def set_cache(key:str,value:Any,expire:int=3600):
    try:
        if isinstance(value,(list,dict)):
            value=json.dumps(value,ensure_ascii=False)
        await redis_client.setex(key,expire,value)
        return True
    except Exception as e:
        print(f'设置缓存失败:{e}')
        return False

if __name__=='__main__':
    import asyncio
    async def main():
        ok = await redis_client.ping()   # 异步 client 必须 await
        print("连接成功" if ok else "连接失败")

    asyncio.run(main())