# FaceNet Face Recognition System Documentation

## Project Overview / 项目概述

A complete DevOps/MLOps course project demonstrating a face recognition application built with FaceNet and MTCNN. The system provides real-time face recognition and enrollment through a web interface, with full integration of modern development practices including Git, DagsHub, Docker, and GitHub Actions.

完整的DevOps/MLOps课程项目，展示了一个使用FaceNet和MTCNN构建的人脸识别应用。该系统通过Web界面提供实时人脸识别和录入功能，并完整集成了现代开发实践，包括Git、DagsHub、Docker和GitHub Actions。

## Technology Stack / 技术栈

| Technology / 技术 | Purpose / 用途 |
|-------------------|----------------|
| FastAPI | Web framework for backend API / 后端API的Web框架 |
| Keras-FaceNet | Face embedding model for feature extraction / 用于特征提取的人脸嵌入模型 |
| MTCNN | Face detection in images / 图像中的人脸检测 |
| TensorFlow | Machine learning backend / 机器学习后端 |
| Docker | Containerization for deployment / 部署容器化 |
| DVC (Data Version Control) | Version control for datasets / 数据集的版本控制 |
| MLflow | Experiment tracking for ML models / ML模型的实验跟踪 |
| GitHub Actions | CI/CD pipeline automation / CI/CD流水线自动化 |
| Cryptography | Data encryption for face images / 人脸图像的数据加密 |

## Core Features / 核心功能

| Feature / 功能 | Description / 描述 |
|----------------|-------------------|
| Real-time Face Recognition | Detect and identify faces from webcam feed in real-time / 从摄像头实时检测和识别人脸 |
| Face Enrollment | Register new faces with name labels / 使用姓名标签注册新人脸 |
| Secure Data Storage | Encrypt stored face images using AES-256 / 使用AES-256加密存储的人脸图像 |
| Web Interface | User-friendly browser-based interface / 基于浏览器的用户友好界面 |
| RESTful API | Programmatic access to recognition and enrollment / 通过编程方式访问识别和录入功能 |

## Project Structure / 项目结构

| Directory/File / 目录/文件 | Purpose / 用途 |
|---------------------------|----------------|
| app/ | Main application code / 主要应用代码 |
| ├── main.py | FastAPI application entry point / FastAPI应用入口点 |
| ├── face_recognition.py | Core face recognition logic / 核心人脸识别逻辑 |
| ├── encryption.py | Data encryption utilities / 数据加密工具 |
| static/ | Frontend assets (HTML, CSS, JS) / 前端资源 |
| tests/ | Unit and integration tests / 单元和集成测试 |
| data/ | Face embeddings and encrypted images / 人脸嵌入和加密图像 |
| scripts/ | Utility scripts for data management / 数据管理的实用脚本 |
| .github/workflows/ | CI/CD pipeline definitions / CI/CD流水线定义 |
| Dockerfile | Container build instructions / 容器构建说明 |
| docker-compose.yml | Multi-container deployment / 多容器部署 |

## Development & Deployment / 开发与部署

| Step / 步骤 | Command / 命令 | Purpose / 用途 |
|-------------|----------------|----------------|
| Local Development | `uvicorn app.main:app --reload` | Run development server / 运行开发服务器 |
| Testing | `pytest` | Run test suite / 运行测试套件 |
| Code Quality | `flake8 app/ tests/` | Code linting and style checking / 代码检查和风格检查 |
| Docker Build | `docker-compose up --build` | Build and run containers / 构建并运行容器 |
| Data Versioning | `dvc add data` | Track datasets with DVC / 使用DVC跟踪数据集 |
| CI/CD | Automatic on git push | Automated testing and deployment / 自动化测试和部署 |

## Configuration / 配置

| Environment Variable / 环境变量 | Purpose / 用途 | Example / 示例 |
|-------------------------------|----------------|----------------|
| ENCRYPTION_KEY | AES-256 key for data encryption / 用于数据加密的AES-256密钥 | 32-byte base64 string |
| APP_HOST | Application host binding / 应用主机绑定 | 0.0.0.0 |
| APP_PORT | Application port / 应用端口 | 8000 |
| FACE_RECOGNITION_THRESHOLD | Similarity threshold for face matching / 人脸匹配的相似度阈值 | 0.6 |

## API Endpoints / API端点

| Endpoint / 端点 | Method / 方法 | Purpose / 用途 |
|-----------------|---------------|----------------|
| / | GET | Serve web interface / 提供Web界面 |
| /recognize | POST | Recognize faces from uploaded image / 从上传图像识别人脸 |
| /recognize_base64 | POST | Recognize faces from base64 image / 从base64图像识别人脸 |
| /enroll | POST | Enroll new face with name / 使用姓名录入新人脸 |
| /enroll_base64 | POST | Enroll new face with base64 image / 使用base64图像录入新人脸 |
| /health | GET | Health check endpoint / 健康检查端点 |
