# ClassManer 后端安装指南

## 环境要求

- Python 3.12+
- MySQL 5.7+
- 虚拟环境工具(推荐 virtualenv)

## 安装步骤

1. 克隆项目
```bash
git clone https://github.com/HuYihe2008/ClassManner-V1.0.git
cd ClassManner-V1.0/API
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
打开 `config/db.py` 并配置数据库连接信息
```dotenv
#配置区域
DATABASE_USER = "数据库用户名"
DATABASE_PASSWORD = "数据库密码"
DATABASE_HOST = "数据库访问地址"
DATABASE_PORT = "数据库端口（一般为3306）"
DATABASE_NAME = "数据库名"
```
`推荐将API与数据库在同一台服务器上，这样便于管理，且提高数据库安全性，因为这样访问地址可以使用localhost`



6. 启动服务器并初始化数据库
```bash
uvicorn main:app --reload
```

## 项目结构
```
backend/
├── app/
│   ├── models/     # 数据模型
│   ├── schemas/    # 数据验证
│   ├── api/        # API路由
│   ├── core/       # 核心配置
│   └── utils/      # 工具函数
├── tests/          # 测试文件
└── main.py         # 入口文件
```

## 数据库迁移
（相关功能暂未开发）
