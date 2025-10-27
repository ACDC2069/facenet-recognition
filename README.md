# FaceNet人脸识别项目 (DevOps/MLOps课程大作业)

本项目为DevOps/MLOps课程大作业项目，旨在通过一个实际的人脸识别应用，全面展示从开发、测试、部署到监控的整个生命周期管理。项目基于FaceNet实现，提供了一个简洁的Web界面用于实时人脸识别和录入，并深度整合了Git、DagsHub、Docker、GitHub Actions等现代工程实践。

## 项目特色

- **实时人脸识别与录入**：通过Web摄像头实时识别已知人脸，并能动态录入新面孔。
- **MLOps集成**：使用 **DagsHub** 和 **DVC** 对人脸数据集和模型进行版本控制，实现数据和模型的溯源与复现。
- **Git专业工作流**：严格遵循 `main`, `staging`, `dev`, `feature` 的分支模型，规范开发流程。
- **自动化CI/CD**：利用 **GitHub Actions** 实现自动化代码检查（Linting）、单元测试、Docker镜像构建和安全扫描。
- **容器化部署**：使用 **Docker** 和 **Docker Compose** 将应用打包，实现环境一致性与一键部署。
- **配置与代码分离**：通过 `.env` 文件管理敏感配置（如加密密钥），遵循十二因子应用原则。
- **数据安全**：对存储的人脸图像进行对称加密，并通过 **GitHub Secrets** 安全管理密钥。

## 技术栈

| 类别 | 技术/工具 |
| :--- | :--- |
| **机器学习** | `keras-facenet`, `mtcnn`, `tensorflow` |
| **后端服务** | `FastAPI`, `uvicorn` |
| **前端界面** | `HTML`, `CSS`, `JavaScript` |
| **版本控制** | `Git`, `GitHub` |
| **数据与模型版本控制** | `DagsHub`, `DVC` |
| **CI/CD** | `GitHub Actions` |
| **容器化** | `Docker`, `Docker Compose` |
| **代码质量与测试** | `flake8`, `pytest` |
| **安全** | `cryptography`, `GitHub Secrets` |

## 项目结构

详细的项目文件结构说明请参见 `project_structure.md` 文件。