from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message:str='success',data=None):  
    content={
        'code':200,
        'message':message,
        'data':data
    }
    '''
    jsonable_encoder 把 data 里不可 JSON 序列化的对象（如 Pydantic 模型、ORM 对象、datetime、Decimal 等）转成可序列化的 dict/list
    '''
    return JSONResponse(content=jsonable_encoder(content)
    )