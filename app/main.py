"""
FastAPI主应用
提供人脸识别和录入的Web API
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image
import io
import base64
from app.face_recognition import FaceRecognitionSystem
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="FaceNet人脸识别系统", version="1.0.0")

# 初始化人脸识别系统
face_system = FaceRecognitionSystem()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回前端主页面"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    """
    识别图像中的人脸

    Args:
        file: 上传的图像文件

    Returns:
        识别结果列表
    """
    try:
        # 读取图像
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # 转换为RGB（如果需要）
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 执行识别
        results = face_system.recognize_image(image)

        return JSONResponse(content={"results": results})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recognize_base64")
async def recognize_base64(data: dict):
    """
    识别Base64编码的图像中的人脸

    Args:
        data: 包含base64图像数据的字典

    Returns:
        识别结果列表
    """
    try:
        # 解码Base64图像
        image_data = data.get('image', '')
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # 转换为RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 执行识别
        results = face_system.recognize_image(image)

        return JSONResponse(content={"results": results})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/enroll")
async def enroll(name: str = Form(...), file: UploadFile = File(...)):
    """
    录入新人脸

    Args:
        name: 人员姓名
        file: 上传的图像文件

    Returns:
        录入结果
    """
    try:
        # 读取图像
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # 转换为RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 执行录入
        success = face_system.enroll_face(image, name)

        if success:
            return JSONResponse(content={
                "success": True,
                "message": f"成功录入 {name} 的人脸信息"
            })
        else:
            return JSONResponse(content={
                "success": False,
                "message": "未检测到人脸，请重试"
            }, status_code=400)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/enroll_base64")
async def enroll_base64(data: dict):
    """
    通过Base64编码的图像录入新人脸

    Args:
        data: 包含name和base64图像数据的字典

    Returns:
        录入结果
    """
    try:
        name = data.get('name', '')
        if not name:
            raise HTTPException(status_code=400, detail="姓名不能为空")

        # 解码Base64图像
        image_data = data.get('image', '')
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # 转换为RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 执行录入
        success = face_system.enroll_face(image, name)

        if success:
            return JSONResponse(content={
                "success": True,
                "message": f"成功录入 {name} 的人脸信息"
            })
        else:
            return JSONResponse(content={
                "success": False,
                "message": "未检测到人脸，请重试"
            }, status_code=400)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "enrolled_faces": len(face_system.names)}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', '8000'))
    uvicorn.run(app, host=host, port=port)

