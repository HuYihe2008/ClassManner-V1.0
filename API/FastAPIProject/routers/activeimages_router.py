import traceback

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import json
import os
import uuid

from models.activeimages import ActiveImage
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
async def create_active_image(
    data: dict = Body(..., description="包含title、content和images的JSON对象"),
    db: Session = Depends(get_db)
):
    try:
        title = data.get("title")
        content = data.get("content")
        images = data.get("images", [])

        if not isinstance(images, list):
            return JSONResponse(
                status_code=400,
                content={"status": "Failed", "message": "images参数必须为数组类型"}
            )

        if not all([title, content]):
            return JSONResponse(
                status_code=400,
                content={"status": "Failed", "message": "标题和内容不能为空"}
            )

        new_image = ActiveImage(
            title=title,
            content=content,
            images=json.dumps(images)
        )

        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": {
                    "id": new_image.id,
                    "title": new_image.title,
                    "content": new_image.content,
                    "images": images
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"创建失败: {str(e)}"}
        )

@router.get("/")
async def get_all_active_images(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    try:
        offset = (page - 1) * page_size
        total = db.query(ActiveImage).count()
        actives = db.query(ActiveImage).offset(offset).limit(page_size).all()

        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": [
                    {
                        "id": active.id,
                        "title": active.title,
                        "content": active.content,
                        "images": json.loads(active.images)
                    } for active in actives
                ],
                "pagination": {
                    "total": total,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        print(f"删除操作异常: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"查询失败: {str(e)}"}
        )

@router.get("/{active_id}")
async def get_single_active_image(
    active_id: int,
    db: Session = Depends(get_db)
):
    try:
        active = db.query(ActiveImage).filter(ActiveImage.id == active_id).first()
        if not active:
            return JSONResponse(
                status_code=404,
                content={"status": "Failed", "message": "未找到该活动"}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": {
                    "id": active.id,
                    "title": active.title,
                    "content": active.content,
                    "images": json.loads(active.images)
                }
            }
        )
    except Exception as e:
        print(f"删除操作异常: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"查询失败: {str(e)}"}
        )


@router.post("/upload")
async def upload_active_images(
    file: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        UPLOAD_DIR = "database/activeimages"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        allowed_types = ["image/jpeg", "image/png"]
        urls = []
        
        for file in file:
            if file.content_type not in allowed_types:
                raise HTTPException(status_code=400, detail=f"文件 {file.filename} 类型不支持")
            
            file_ext = os.path.splitext(file.filename)[1]
            new_filename = f"{uuid.uuid4().hex}{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, new_filename)
            
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            urls.append(f"static/activeimages/{new_filename}")
            
        return JSONResponse(
            status_code=200,
            content={"status": "Success", "data": urls}
        )
    except Exception as e:
        print(f"删除操作异常: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"文件上传失败: {str(e)}"}
        )

@router.put("/{active_id}")
async def update_active_image(
    active_id: int,
    data: dict = Body(..., description="包含title、content和images的更新数据"),
    db: Session = Depends(get_db)
):
    try:
        active = db.query(ActiveImage).filter(ActiveImage.id == active_id).first()
        if not active:
            return JSONResponse(
                status_code=404,
                content={"status": "Failed", "message": "未找到该活动"}
            )

        title = data.get("title")
        content = data.get("content")
        images = data.get("images", [])

        if not isinstance(images, list):
            return JSONResponse(
                status_code=400,
                content={"status": "Failed", "message": "images参数必须为数组类型"}
            )

        if not all([title, content]):
            return JSONResponse(
                status_code=400,
                content={"status": "Failed", "message": "标题和内容不能为空"}
            )

        active.title = title
        active.content = content
        active.images = json.dumps(images)

        db.commit()
        db.refresh(active)

        return JSONResponse(
            status_code=200,
            content={
                "status": "Success",
                "data": {
                    "id": active.id,
                    "title": active.title,
                    "content": active.content,
                    "images": images
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"更新失败: {str(e)}"}
        )

@router.delete("/image/{image_url}")
async def delete_single_image(
        image_url: str,
        db: Session = Depends(get_db)
):
    try:
        from urllib.parse import unquote
        import shutil
        import re

        # 类型验证确保接收字符串
        if not isinstance(image_url, str):
            raise HTTPException(status_code=400, detail="Invalid image_url format")

        # 解码URL并提取文件名
        decoded_url = unquote(image_url)
        decoded_url = decoded_url.replace('/static/activeimages/', '')
        filename = os.path.basename(decoded_url)

        # 删除本地图片文件
        file_path = os.path.join("database/activeimages", filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        # 更新所有关联的activeimages记录
        all_records = db.query(ActiveImage).all()
        pattern = re.compile(r'static/activeimages/' + re.escape(filename) + r'(?:\?.*)?$')

        for record in all_records:
            # 统一转换为列表并过滤非字符串元素
            images = json.loads(record.images) if isinstance(record.images, str) else record.images
            valid_images = [img for img in images if isinstance(img, str)]
            new_images = [img for img in valid_images if not pattern.search(img)]
            if len(new_images) < len(images):
                record.images = json.dumps(new_images)
                db.add(record)

        db.commit()

        return JSONResponse(
            status_code=200,
            content={"status": "Success", "message": "图片删除成功"}
        )
    except Exception as e:
        db.rollback()
        print(f"删除操作异常: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"删除失败: {str(e)}"}
        )

@router.delete("/{active_id}")
async def delete_active_image(
    active_id: int,
    db: Session = Depends(get_db)
):
    try:
        active = db.query(ActiveImage).filter(ActiveImage.id == active_id).first()
        if not active:
            return JSONResponse(
                status_code=404,
                content={"status": "Failed", "message": "未找到该活动"}
            )

        db.delete(active)
        db.commit()

        return JSONResponse(
            status_code=200,
            content={"status": "Success", "message": "活动删除成功"}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "Failed", "message": f"删除失败: {str(e)}"}
        )

