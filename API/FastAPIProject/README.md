# Manner Class 后台管理系统 API

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 项目概述

本系统是为Manner Class艺术培训学校定制的后台管理API，基于FastAPI框架开发，提供完整的用户管理、作品展示、留言通知等功能模块。

## 核心功能模块

- 👨💻 用户管理系统
- 🖼️ 活动图片/优秀作品展示
- 📝 匿名留言板
- 🔔 系统通知管理
- 🔐 JWT身份验证

## 技术栈

```text
FastAPI | MySQL | SQLAlchemy | Pymysql | JWT
```

## 安装指南

```bash
# 克隆项目
git clone https://github.com/your-repo/manner-class-api.git

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload
```

## 环境配置

1. 打开 `./config/db.py` 文件
2. 修改以下数据库连接参数：
```python
DATABASE_USER = "用户名"
DATABASE_PASSWORD = "密码"
DATABASE_HOST = "数据库地址"
DATABASE_PORT = "3306"
DATABASE_NAME = "数据库名"
```
3. 安全注意事项：
   - 不要将包含敏感信息的配置文件提交到版本控制
   - 生产环境建议使用环境变量注入敏感信息

## API文档

访问本地调试文档：
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### 主要接口

| 模块        | 端点                      | 方法   | 描述               |
|-----------|-------------------------|------|------------------|
| 用户管理     | /api/users/create       | POST | 创建新用户           |
| 活动图片     | /api/active-images      | GET  | 获取活动图片列表       |
| 优秀作品     | /api/excellent-works    | GET  | 获取优秀作品列表       |
| 匿名留言     | /api/anonymous-messages | POST | 提交匿名留言         |
| 系统通知     | /api/notice             | GET  | 获取最新系统通知       |

## 项目结构

```
├── main.py               # 应用入口
├── database.py           # 数据库配置
├── requirements.txt      # 依赖清单
│
├── routers/              # 路由模块
│   ├── user_router.py     # 用户路由
│   ├── activeimages_router.py # 活动图片
│   └── ...
│
├── models/               # 数据模型
│   ├── user.py           # 用户模型
│   ├── activeimages.py   # 活动图片模型
│   └── ...
│
└── database/             # 静态资源
    ├── activeimages/     # 活动图片存储
    └── excellentworks/   # 优秀作品存储
```

## 开发者指南

欢迎贡献代码！请遵循以下规范：
1. 使用Black代码格式化
2. 新功能开发请创建feature分支
3. 提交前确保通过单元测试
4. 更新API文档说明

---

© 2024 Manner Class. All rights reserved.