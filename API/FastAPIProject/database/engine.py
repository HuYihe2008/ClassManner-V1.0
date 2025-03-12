from sqlalchemy import create_engine

# 数据库连接配置
DATABASE_URL = "mysql+pymysql://your_user:your_password@your_host:your_port/your_database"  # 修改：替换为实际的数据库连接信息

# 创建数据库引擎
engine = create_engine(DATABASE_URL, pool_pre_ping=True)