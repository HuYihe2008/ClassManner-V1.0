from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/latest")
async def get_latest_app():
    try:
        # 修改为绝对路径
        app_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "app")
        os.makedirs(app_dir, exist_ok=True)
        
        files = os.listdir(app_dir)
        if not files:
            raise HTTPException(status_code=404, detail="没有找到可用的客户端安装包")
        
        # 按版本号排序（假设文件名格式为 app_v1.0.0.exe）
        latest_app = sorted(files, reverse=True)[0]
        file_path = os.path.join(app_dir, latest_app)
        
        # 指定正确的媒体类型和文件名
        return FileResponse(
            path=file_path,
            filename=latest_app,
            media_type="application/vnd.microsoft.portable-executable"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载失败: {str(e)}")
