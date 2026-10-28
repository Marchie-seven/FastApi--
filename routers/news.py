from fastapi import APIRouter

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
async def get_categories(skip:int=0, limit:int=100):
    return {
        "code":200,
        "message":"获取新闻分类成功",
        "data":"新闻分类列表"
    }









