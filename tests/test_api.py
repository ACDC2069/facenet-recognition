"""
API端点测试
"""
import pytest
from fastapi.testclient import TestClient
import os
import sys
import base64
from io import BytesIO
from PIL import Image

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 设置测试环境变量
os.environ['ENCRYPTION_KEY'] = 'test-key-for-testing-only-32bytes='

from app.main import app

client = TestClient(app)


@pytest.fixture
def sample_image_bytes():
    """创建测试用的图像字节数据"""
    img = Image.new('RGB', (640, 480), color='white')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


@pytest.fixture
def sample_image_base64():
    """创建测试用的Base64编码图像"""
    img = Image.new('RGB', (640, 480), color='white')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    encoded = base64.b64encode(img_bytes.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"


def test_read_root():
    """测试根路径返回HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_health_check():
    """测试健康检查端点"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "enrolled_faces" in data


def test_recognize_endpoint(sample_image_bytes):
    """测试识别端点"""
    files = {"file": ("test.jpg", sample_image_bytes, "image/jpeg")}
    response = client.post("/recognize", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)


def test_recognize_base64_endpoint(sample_image_base64):
    """测试Base64识别端点"""
    response = client.post(
        "/recognize_base64",
        json={"image": sample_image_base64}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)


def test_enroll_endpoint(sample_image_bytes):
    """测试录入端点"""
    files = {"file": ("test.jpg", sample_image_bytes, "image/jpeg")}
    data = {"name": "TestUser"}
    
    response = client.post("/enroll", data=data, files=files)
    
    # 由于是空白图像，可能检测不到人脸，返回400
    assert response.status_code in [200, 400]


def test_enroll_base64_endpoint(sample_image_base64):
    """测试Base64录入端点"""
    response = client.post(
        "/enroll_base64",
        json={"name": "TestUser", "image": sample_image_base64}
    )
    
    # 由于是空白图像，可能检测不到人脸，返回400
    assert response.status_code in [200, 400]


def test_enroll_without_name(sample_image_base64):
    """测试没有姓名的录入请求"""
    response = client.post(
        "/enroll_base64",
        json={"image": sample_image_base64}
    )
    
    assert response.status_code == 400


def test_invalid_image_data():
    """测试无效的图像数据"""
    response = client.post(
        "/recognize_base64",
        json={"image": "invalid-base64-data"}
    )
    
    assert response.status_code == 500

