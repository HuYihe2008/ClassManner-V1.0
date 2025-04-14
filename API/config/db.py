#配置区域

'''
DATABASE_USER = "mannerdatabase"
DATABASE_PASSWORD = "pcO4BuBloOpp0sak"
DATABASE_HOST = "mysql.sqlpub.com"
DATABASE_PORT = "3306"
DATABASE_NAME = "mannerdatabase"

'''
DATABASE_USER = "classmaner"
DATABASE_PASSWORD = "123456"
DATABASE_HOST = "localhost"
DATABASE_PORT = "3306"
DATABASE_NAME = "classmaner"

#合成请求链接
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?charset=utf8mb4"