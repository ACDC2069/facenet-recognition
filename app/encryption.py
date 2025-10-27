"""
数据加密和解密工具模块
使用Fernet对称加密保护人脸图像数据
"""
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


class EncryptionManager:
    """加密管理器"""

    def __init__(self):
        """初始化加密管理器，从环境变量加载密钥"""
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY not found in environment variables")
        self.cipher = Fernet(key.encode())

    def encrypt(self, data: bytes) -> bytes:
        """
        加密数据

        Args:
            data: 原始字节数据

        Returns:
            加密后的字节数据
        """
        return self.cipher.encrypt(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        解密数据

        Args:
            encrypted_data: 加密的字节数据

        Returns:
            解密后的原始字节数据
        """
        return self.cipher.decrypt(encrypted_data)

    def encrypt_file(self, input_path: str, output_path: str):
        """
        加密文件

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
        """
        with open(input_path, 'rb') as f:
            data = f.read()
        encrypted_data = self.encrypt(data)
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

    def decrypt_file(self, input_path: str, output_path: str):
        """
        解密文件

        Args:
            input_path: 加密文件路径
            output_path: 输出文件路径
        """
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()
        data = self.decrypt(encrypted_data)
        with open(output_path, 'wb') as f:
            f.write(data)


def generate_key() -> str:
    """
    生成新的加密密钥

    Returns:
        Base64编码的密钥字符串
    """
    return Fernet.generate_key().decode()

