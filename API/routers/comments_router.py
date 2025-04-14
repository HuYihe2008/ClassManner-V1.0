from fastapi import APIRouter, Depends, Body, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models.comments import Comment
import jwt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
async def create_comment(
    data: dict = Body(...),
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        # 验证token获取用户信息
        token = authorization.split(" ")[1]
        secret_key = "114514"
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        comment = Comment(
            content=data.get("content"),
            user_id=data.get("user_id"),
            user_name=data.get("user_name"),
            user_email=payload.get("email"),
            target_id=data.get("target_id"),
            target_type=data.get("target_type")
        )
        
        db.add(comment)
        db.commit()
        db.refresh(comment)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": {
                    "id": comment.id,
                    "content": comment.content,
                    "user_name": comment.user_name,
                    "user_email": comment.user_email,
                    "created_at": comment.created_at.isoformat()
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": str(e)}
        )

@router.get("/list/{target_type}/{target_id}")
async def get_comments(
    target_type: str,
    target_id: int,
    db: Session = Depends(get_db)
):
    try:
        comments = db.query(Comment).filter(
            Comment.target_type == target_type,
            Comment.target_id == target_id
        ).all()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": [{
                    "id": comment.id,
                    "content": comment.content,
                    "user_name": comment.user_name,
                    "user_email": comment.user_email,
                    "user_id": comment.user_id,
                    "created_at": comment.created_at.isoformat()
                } for comment in comments]
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": str(e)}
        )

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        token = authorization.split(" ")[1]
        secret_key = "114514"
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            return JSONResponse(
                status_code=404,
                content={"status": "Failed", "message": "评论不存在"}
            )
            
        # 验证是否为评论作者或教师
        user = db.query(User).filter(User.email == payload.get("email")).first()
        if user.identity != "teacher" and user.id != comment.user_id:
            return JSONResponse(
                status_code=403,
                content={"status": "Failed", "message": "无权限删除此评论"}
            )
            
        db.delete(comment)
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"status": "Success", "message": "评论已删除"}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": str(e)}
        )
