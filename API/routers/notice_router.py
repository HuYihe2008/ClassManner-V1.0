import traceback
from fastapi import APIRouter, Depends, HTTPException, Body, Query, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from models.notice import Notice
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
async def create_message(
    data: dict = Body(..., description="通知内容"),
    db: Session = Depends(get_db)
):
    try:
        content = data.get("content")
        if not content:
            return JSONResponse(
                status_code=400,
                content={"status": "Failed", "message": "内容不能为空"}
            )

        new_message = Notice(content=content)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": {
                    "id": new_message.id,
                    "content": new_message.content,
                    "timestamp": new_message.timestamp.isoformat()
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"创建失败: {str(e)}"}
        )

@router.get("/get")
async def get_messages(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        offset = (page - 1) * per_page
        messages = db.query(Notice)\
            .order_by(Notice.timestamp.desc())\
            .offset(offset)\
            .limit(per_page)\
            .all()

        total = db.query(Notice).count()

        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": [
                    {
                        "id": msg.id,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat()
                    } for msg in messages
                ],
                "pagination": {
                    "total": total,
                    "page": page,
                    "per_page": per_page
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"获取失败: {str(e)}"}
        )

@router.put("/update/{message_id}")
async def update_message(
    message_id: int,
    data: dict = Body(..., description="新通知内容"),
    db: Session = Depends(get_db)
):
    try:
        content = data.get("content")
        if not content:
            return JSONResponse(
                status_code=400,
                content={"status": "Failed", "message": "内容不能为空"}
            )

        message = db.query(Notice).filter(Notice.id == message_id).first()
        if not message:
            return JSONResponse(
                status_code=404,
                content={"status": "Failed", "message": "通知不存在"}
            )

        message.content = content
        db.commit()

        return JSONResponse(
            status_code=200,
            content={"status": "Success", "message": "更新成功"}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"更新失败: {str(e)}"}
        )

@router.delete("/delete/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    try:
        message = db.query(Notice).filter(Notice.id == message_id).first()
        if not message:
            return JSONResponse(
                status_code=404,
                content={"status": "Failed", "message": "通知不存在"}
            )

        db.delete(message)
        db.commit()

        return JSONResponse(
            status_code=200,
            content={"status": "Success", "message": "删除成功"}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"删除失败: {str(e)}"}
        )

@router.get("/get/{message_id}")
async def get_single_message(
    message_id: int = Path(..., ge=1, description="通知ID"),
    db: Session = Depends(get_db)
):
    try:
        message = db.query(Notice).filter(Notice.id == message_id).first()
        if not message:
            return JSONResponse(
                status_code=404,
                content={"status": "Failed", "message": "通知不存在"}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": {
                    "id": message.id,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat()
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"查询失败: {str(e)}"}
        )