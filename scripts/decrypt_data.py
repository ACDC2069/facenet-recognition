"""
数据解密脚本
用于解密人脸图像数据（仅用于调试）
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.encryption import EncryptionManager
from dotenv import load_dotenv

load_dotenv()


def decrypt_directory(input_dir: str, output_dir: str):
    """
    解密目录中的所有加密文件

    Args:
        input_dir: 输入目录路径（加密文件）
        output_dir: 输出目录路径（解密文件）
    """
    manager = EncryptionManager()
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.enc'):
                file_path = os.path.join(root, filename)
                
                # 构建输出路径（移除.enc扩展名）
                relative_path = os.path.relpath(file_path, input_dir)
                output_filename = relative_path[:-4]  # 移除.enc
                output_path = os.path.join(output_dir, output_filename)
                
                # 确保输出子目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # 解密文件
                try:
                    manager.decrypt_file(file_path, output_path)
                    print(f"已解密: {filename} -> {os.path.basename(output_path)}")
                except Exception as e:
                    print(f"解密失败 {filename}: {e}")


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python decrypt_data.py <输入目录> <输出目录>")
        print("示例: python decrypt_data.py ./data/images ./decrypted_images")
        print("\n警告: 此脚本仅用于调试目的，请勿在生产环境使用!")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录不存在: {input_dir}")
        sys.exit(1)
    
    print(f"开始解密目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    
    decrypt_directory(input_dir, output_dir)
    
    print("解密完成!")


if __name__ == "__main__":
    main()

