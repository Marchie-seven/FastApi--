#新闻相关的缓存方法：新闻分类的读取和写入
#key-value
from typing import Dict, Any, Optional

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY="news:categories"
NEWS_LIST_KEY="news:list"

#获取新闻分类缓存方法
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)

#写入新闻分类缓存方法:缓存的数据，过期的时间
#分类：配置 7200 列表：600详情：1800验证码：120
async def set_cache_categories(data:list[Dict[str,Any]],expire: int=7200):
    return await set_cache(CATEGORIES_KEY,data,expire)

#写入缓存方法-关于新闻列表 key=news_list:分类的id：页码：每页数量+列表数据+过期时间
async def set_cached_news(category_id:Optional[int],page:int,page_size:int,news_list:list[Dict[str,Any]],expire: int=600):
    #调用封装的redis的设置方法，存新闻列表到缓存
    category_part=category_id if category_id is not None else "all"
    key=f"{NEWS_LIST_KEY}:{category_part}:{page}:{page_size}"
    return await set_cache(key,news_list,expire)
#读取缓存-新闻列表
async def get_cached_news_list(category_id:Optional[int],page:int,page_size:int):
    category_part=category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_KEY}:{category_part}:{page}:{page_size}"
    return await get_json_cache(key)






















