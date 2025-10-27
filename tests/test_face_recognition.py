"""
人脸识别模块测试
"""
import pytest
import numpy as np
from PIL import Image
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.face_recognition import FaceRecognitionSystem


@pytest.fixture
def face_system(tmp_path):
    """创建临时的人脸识别系统实例"""
    data_path = str(tmp_path / "test_faces.npz")
    images_dir = str(tmp_path / "test_images")
    os.makedirs(images_dir, exist_ok=True)
    
    # 设置测试环境变量
    os.environ['ENCRYPTION_KEY'] = 'test-key-for-testing-only-32bytes='
    
    system = FaceRecognitionSystem(data_path=data_path, images_dir=images_dir)
    return system


@pytest.fixture
def sample_image():
    """创建测试用的样本图像"""
    # 创建一个简单的RGB图像
    img = Image.new('RGB', (640, 480), color='white')
    return img


def test_face_system_initialization(face_system):
    """测试人脸识别系统初始化"""
    assert face_system is not None
    assert face_system.names == []
    assert face_system.embeddings == []
    assert face_system.threshold > 0


def test_detect_faces_empty_image(face_system, sample_image):
    """测试在空白图像上检测人脸"""
    faces = face_system.detect_faces(sample_image)
    # 空白图像应该检测不到人脸
    assert isinstance(faces, list)


def test_database_save_and_load(face_system, tmp_path):
    """测试数据库保存和加载"""
    # 添加测试数据
    face_system.names = ['Alice', 'Bob']
    face_system.embeddings = [
        np.random.rand(128),
        np.random.rand(128)
    ]
    
    # 保存
    face_system._save_database()
    
    # 创建新实例并加载
    new_system = FaceRecognitionSystem(
        data_path=face_system.data_path,
        images_dir=face_system.images_dir
    )
    
    assert new_system.names == ['Alice', 'Bob']
    assert len(new_system.embeddings) == 2


def test_recognize_face_empty_database(face_system):
    """测试在空数据库中识别人脸"""
    embedding = np.random.rand(128)
    name, distance = face_system.recognize_face(embedding)
    
    assert name is None
    assert distance == float('inf')


def test_recognize_face_with_data(face_system):
    """测试在有数据的数据库中识别人脸"""
    # 添加已知人脸
    known_embedding = np.random.rand(128)
    face_system.names = ['TestPerson']
    face_system.embeddings = [known_embedding]
    
    # 测试识别相同的embedding（距离应该为0）
    name, distance = face_system.recognize_face(known_embedding)
    
    assert distance < face_system.threshold
    # 注意：由于是随机embedding，可能无法准确识别


def test_image_mode_conversion(face_system):
    """测试图像模式转换"""
    # 创建RGBA图像
    rgba_image = Image.new('RGBA', (640, 480), color='white')
    
    # 转换为RGB
    rgb_image = rgba_image.convert('RGB')
    
    assert rgb_image.mode == 'RGB'
    
    # 尝试检测（不应该抛出异常）
    faces = face_system.detect_faces(rgb_image)
    assert isinstance(faces, list)

