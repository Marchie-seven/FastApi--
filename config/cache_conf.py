import json
from dataclasses import asdict
from typing import Any
import logging
import redis.asyncio as redis
from sqlalchemy.util import await_

REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_DB=0

#创建redis连接对象
redis_client=redis.Redis(
    host=REDIS_HOST,#redis服务器主机地址
    port=REDIS_PORT,#redis服务器端口号
    db=REDIS_DB,#redis数据库编号0到15
    decode_responses=True,#是否将redis返回的字符串解码为utf-8编码
    protocol=2,#redis协议版本2
)
logger=logging.getLogger(__name__)
#设置和读取(字符串和列表或字典)“[{}]”
#读取：字符串
async def get_cache(key: str):
    # return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        logging.error(f"读取缓存失败：{e}")
        return None

#读取：列表或字典
async def get_json_cache(key: str):
    try:
        data=await redis_client.get(key)
        if data:
            return json.loads(data)#反序列化:将json字符串转换为python对象
        return None
    except Exception as e:
        print(f"读取缓存失败：{e}")
        return None

# 设置缓存 setex(key,expire,value)
async def set_cache(key: str,value: Any,expire:int=3600):
    try:
        if isinstance(value,(dict,list)):
            #转字符串再存
            value=json.dumps(value,ensure_ascii=False)#序列化:将python对象转换为json字符串，中文不转义
        await redis_client.setex(key,expire,value)#设置缓存，过期时间为expire秒，值为value
        return True
    except Exception as e:
        logger.error(f"设置缓存失败：{e}")
        return False
















