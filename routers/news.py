from fastapi import APIRouter,Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine

from config.db_conf import get_db
from crud import news
# 创建api router实例
# prefix路由前缀(API接口规范文档)
# tags分组标签
router = APIRouter(prefix="/api/news", tags=["news"])
# 接口实现流程
# 1.定义模块化路由->api接口规范文档
# 2.定义模型类->数据库表（数据库设计文档）
# 3.在crud文件夹里面创建文件来封装数据库的方法
# 4.在路由处理函数里面调用crud封装好的响应结果

@router.get("/categories")
async def get_categories(db:AsyncSession=Depends(get_db),skip:int=0, limit:int=100):
    #先获取数据库里面的新闻分类数据->先定义模型类->封装查询数据的方法
    categories=await news.get_categories(db,skip,limit)
    return {
        "code":200,
        "message":"获取新闻分类成功",
        "data":categories
    }
@router.get("/list")
async def get_news_list(
        category_id:int=Query(...,alias="categoryId"),
        page:int=1,
        page_size:int=Query(10,alias="pageSize",le=100),
        db:AsyncSession=Depends(get_db),
):
    offset = (page-1)*page_size
    new_list=await news.get_news_list(db,category_id,offset,page_size)
    total=await news.get_news_count(db,category_id)
    #跳过的+当前列表里面的<总数量
    has_more=offset+len(new_list)<total

    #思路：处理分页的规则->查询新闻列表->计算总量->计算是否还有更多
    return {
        "code":200,
        "message":"获取新闻列表成功",
        "data":{
            "list":new_list,
            "total":total,
            "hasMore":has_more
        }
    }








