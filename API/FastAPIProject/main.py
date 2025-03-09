from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from routers import user_router, activeimages_router, excellentworks_router, anonymous_messages_router, notice_router
from sqlalchemy import text  # 新增：导入 text 函数
from fastapi.staticfiles import StaticFiles

# 创建 FastAPI 应用
app = FastAPI(debug=True)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# 创建数据库表（如果不存在）
Base.metadata.create_all(bind=engine)

# 检查数据库连接
def check_database_connection():
    try:
        db = SessionLocal()
        # 执行一个简单的查询以检查连接
        db.execute(text("SELECT 1"))  # 修改：使用 text 函数包装 SQL 表达式
        db.close()
        print("Database connection successful")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

check_database_connection()

# 注册路由
app.include_router(user_router.router, prefix="/api/users")
app.include_router(activeimages_router.router, prefix="/api/active-images")
app.include_router(excellentworks_router.router,prefix="/api/excellent-works")
app.include_router(anonymous_messages_router.router, prefix="/api/anonymous-messages")
app.include_router(notice_router.router, prefix="/api/notice")

# 添加静态文件服务配置
app.mount("/static/activeimages", StaticFiles(directory="database/activeimages"), name="activeimages")
app.mount("/static/excellentworks", StaticFiles(directory="database/excellentworks"), name="excellentworks")

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
