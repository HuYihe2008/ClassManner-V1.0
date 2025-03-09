import jwt
from fastapi import APIRouter, Depends, Body, Query, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional  # 新增Optional导入

from models.user import User
from database import SessionLocal


router = APIRouter()

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_user(
    user_data: dict = Body(None, description="用户创建信息，包含 name, email, password, identity"),
    name: str = Query(None, description="用户名"),
    email: str = Query(None, description="邮箱"),
    password: str = Query(None, description="密码"),
    identity: str = Query(None, description="身份"),
    db: Session = Depends(get_db)
):
    try:
        # 优先从 Body 中获取数据
        if user_data:
            name = user_data.get("name")
            email = user_data.get("email")
            password = user_data.get("password")
            identity = user_data.get("identity")
        else:
            # 如果 Body 中没有数据，则从 Query 参数中获取
            if not all([name, email, password, identity]):
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "Failed",
                        "message": "所有字段都不能为空！"
                    },
                )

        # 校验字段是否为空
        if not all([name, email, password, identity]):
            return JSONResponse(
                status_code=400,
                content={
                    "status": "Failed",
                    "message": "所有字段都不能为空！"
                },
            )

        # 检查邮箱是否已存在
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return JSONResponse(
                status_code=418,
                content={
                    "status": "Failed",
                    "message": f"Oops! 邮箱被注册啦！"
                },
            )

        # 查询当前最大ID值，并在此基础上加1
        max_id_user = db.query(User).order_by(User.id.desc()).first()
        new_id = max_id_user.id + 1 if max_id_user else 1

        # 创建新用户
        new_user = User(id=new_id, name=name, email=email, password=password, identity=identity)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 返回创建的用户信息（添加 status 字段）
        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "message": [
                    {
                        "message": "用户创建成功！",
                        "id": new_user.id,
                        "name": new_user.name,
                        "email": new_user.email,
                        "identity": new_user.identity,
                    }
                ]
            },
        )
    except Exception as e:
        # 捕获异常并返回失败状态
        return JSONResponse(
            status_code=500,
            content={
                "status": "Failed",
                "message": f"Oops! O.o 哎呀出错了诶～{str(e)}"
            },
        )

@router.post("/login")
def login_user(
    user_data: dict = Body(None, description="用户登录信息，包含 name/email 和 password"),
    name: str = Query(None, description="用户名"),
    email: str = Query(None, description="邮箱"),
    password: str = Query(None, description="密码"),
    db: Session = Depends(get_db)
):
    try:
        # 检查是否提供了用户名或邮箱
        if user_data:
            name = user_data.get("name")
            email = user_data.get("email")
            password = user_data.get("password")
        else:
            if not all([email, password]):
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "Failed",
                        "message": "必须提供邮箱和密码"
                    },
                )

        # 验证 password 是否为空
        if not password:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "Failed",
                    "message": "密码不能为空！"
                },
            )

        if not name and not email:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "Failed",
                    "message": "邮箱不能为空！"
                },
            )

        # 根据提供的字段查询用户
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "Failed",
                    "message": "邮箱不存在！"
                },
            )

        # 验证密码是否正确
        if user.password != password:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "Failed",
                    "message": "密码错误！"
                },
            )

        # 登录成功，生成 token
        payload = {
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "exp": datetime.utcnow() + timedelta(hours=1)  # token 过期时间
        }
        secret_key = "114514"  # 请替换为实际的密钥
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # 返回用户信息及 token
        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "message": "登陆成功！",
                "token": token
            },
        )
    except Exception as e:
        # 捕获异常并返回失败状态
        return JSONResponse(
            status_code=500,
            content={
                "status": "Failed",
                "message": f"登录过程中发生错误：{str(e)}"
            },
        )

@router.post("/userinfo")
def get_user_info(
    authorization: str = Header(..., description="Bearer Token"),
    db: Session = Depends(get_db)
):
    try:
        # 验证Token格式
        if not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "status": "Failed", 
                    "message": "Token格式不正确"
                }
            )
        
        token = authorization.split(" ")[1]
        
        # 解码Token
        secret_key = "114514"
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_email = payload.get("email")
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"status": "Failed", "message": "Token已过期"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"status": "Failed", "message": "无效的Token"}
            )
        
        # 查询用户信息
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            return JSONResponse(
                status_code=404,
                content={"status": "Failed", "message": "用户不存在"}
            )
        
        # 返回用户信息
        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "identity": user.identity
                }
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"服务器错误: {str(e)}"}
        )