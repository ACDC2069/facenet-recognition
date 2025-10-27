"""
数据加密脚本
用于批量加密人脸图像数据
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


def encrypt_directory(input_dir: str, output_dir: str):
    """
    加密目录中的所有图像文件

    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
    """
    manager = EncryptionManager()
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的图像格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    # 遍历输入目录
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext in image_extensions:
                # 构建输出路径
                relative_path = os.path.relpath(file_path, input_dir)
                output_path = os.path.join(output_dir, relative_path + '.enc')
                
                # 确保输出子目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # 加密文件
                try:
                    manager.encrypt_file(file_path, output_path)
                    print(f"已加密: {filename} -> {os.path.basename(output_path)}")
                except Exception as e:
                    print(f"加密失败 {filename}: {e}")


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python encrypt_data.py <输入目录> <输出目录>")
        print("示例: python encrypt_data.py ./raw_images ./data/images")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录不存在: {input_dir}")
        sys.exit(1)
    
    print(f"开始加密目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    
    encrypt_directory(input_dir, output_dir)
    
    print("加密完成!")


if __name__ == "__main__":
    main()

