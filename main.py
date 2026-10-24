from fastapi import FastAPI
from routers import history, news,users,favorite
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handler import register_exception_handlers

app=FastAPI()

#* 注册异常处理器
register_exception_handlers(app)

#* 解决跨域问题，让前端能够访问后端
origins=[
    'http://localhost',
    'http://localhost:5173',
]
#添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  #允许访问的源
    allow_credentials=True, #允许携带cookie
    allow_methods=['*'], #允许所有请求方式
    allow_headers=['*']  #允许所有请求头
)

@app.get('/')
async def root():
    return {'msg':'hello'}

#* 挂载路由 新闻模块
app.include_router(news.router)


#* 挂载路由 用户模块
app.include_router(users.router)

#* 挂载路由 收藏模块
app.include_router(favorite.router)

#* 挂载路由 历史模块
app.include_router(history.router)