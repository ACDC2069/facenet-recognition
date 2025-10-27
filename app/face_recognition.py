"""
人脸识别核心模块
基于FaceNet和MTCNN实现人脸检测、特征提取和识别
"""
import os
import numpy as np
from PIL import Image
from mtcnn import MTCNN
from keras_facenet import FaceNet
from typing import List, Tuple, Optional
import io
from dotenv import load_dotenv
from app.encryption import EncryptionManager

load_dotenv()


class FaceRecognitionSystem:
    """人脸识别系统"""

    def __init__(self, data_path: str = "data/faces.npz",
                 images_dir: str = "data/images"):
        """
        初始化人脸识别系统

        Args:
            data_path: 人脸特征数据库路径
            images_dir: 人脸图像存储目录
        """
        self.detector = MTCNN()
        self.embedder = FaceNet()
        self.data_path = data_path
        self.images_dir = images_dir
        self.threshold = float(os.getenv('FACE_RECOGNITION_THRESHOLD', '0.6'))
        self.encryption_manager = EncryptionManager()

        # 确保目录存在
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        # 加载已有数据
        self.names = []
        self.embeddings = []
        self._load_database()

    def _load_database(self):
        """从文件加载人脸数据库"""
        if os.path.exists(self.data_path):
            data = np.load(self.data_path, allow_pickle=True)
            self.names = data['names'].tolist()
            self.embeddings = data['embeddings'].tolist()

    def _save_database(self):
        """保存人脸数据库到文件"""
        np.savez(self.data_path,
                 names=np.array(self.names),
                 embeddings=np.array(self.embeddings))

    def detect_faces(self, image: Image.Image) -> List[dict]:
        """
        检测图像中的人脸

        Args:
            image: PIL图像对象

        Returns:
            人脸检测结果列表，每个元素包含box和keypoints
        """
        img_array = np.array(image)
        faces = self.detector.detect_faces(img_array)
        return faces

    def get_embedding(self, image: Image.Image, face_box: dict) -> np.ndarray:
        """
        提取人脸特征向量

        Args:
            image: PIL图像对象
            face_box: 人脸边界框信息

        Returns:
            128维特征向量
        """
        img_array = np.array(image)
        x, y, w, h = face_box['box']
        # 确保坐标不越界
        x, y = max(0, x), max(0, y)
        face = img_array[y:y+h, x:x+w]

        if face.size == 0:
            return None

        # 调整大小到160x160（FaceNet要求）
        face_img = Image.fromarray(face)
        face_img = face_img.resize((160, 160))
        face_array = np.array(face_img)

        # 扩展维度并提取特征
        face_array = np.expand_dims(face_array, axis=0)
        embedding = self.embedder.embeddings(face_array)
        return embedding[0]

    def recognize_face(self, embedding: np.ndarray) -> Tuple[Optional[str], float]:
        """
        识别人脸

        Args:
            embedding: 人脸特征向量

        Returns:
            (识别出的姓名, 距离) 如果无法识别则返回(None, distance)
        """
        if len(self.embeddings) == 0:
            return None, float('inf')

        # 计算与所有已知人脸的欧氏距离
        distances = []
        for known_embedding in self.embeddings:
            distance = np.linalg.norm(embedding - known_embedding)
            distances.append(distance)

        min_distance = min(distances)
        min_index = distances.index(min_distance)

        # 如果距离小于阈值，则认为识别成功
        if min_distance < self.threshold:
            return self.names[min_index], min_distance
        else:
            return None, min_distance

    def enroll_face(self, image: Image.Image, name: str) -> bool:
        """
        录入新人脸

        Args:
            image: PIL图像对象
            name: 人员姓名

        Returns:
            是否成功录入
        """
        faces = self.detect_faces(image)
        if len(faces) == 0:
            return False

        # 只使用第一个检测到的人脸
        face_box = faces[0]
        embedding = self.get_embedding(image, face_box)

        if embedding is None:
            return False

        # 保存加密的图像
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_data = img_bytes.getvalue()
        encrypted_data = self.encryption_manager.encrypt(img_data)

        # 生成唯一文件名
        import time
        timestamp = int(time.time() * 1000)
        filename = f"{name}_{timestamp}.enc"
        filepath = os.path.join(self.images_dir, filename)

        with open(filepath, 'wb') as f:
            f.write(encrypted_data)

        # 添加到数据库
        self.names.append(name)
        self.embeddings.append(embedding)
        self._save_database()

        return True

    def recognize_image(self, image: Image.Image) -> List[dict]:
        """
        识别图像中的所有人脸

        Args:
            image: PIL图像对象

        Returns:
            识别结果列表，每个元素包含name, box, confidence
        """
        faces = self.detect_faces(image)
        results = []

        for face in faces:
            embedding = self.get_embedding(image, face)
            if embedding is None:
                continue

            name, distance = self.recognize_face(embedding)
            box = face['box']

            results.append({
                'name': name if name else 'Unknown',
                'box': box,
                'confidence': max(0, 1 - distance)  # 转换为置信度
            })

        return results

