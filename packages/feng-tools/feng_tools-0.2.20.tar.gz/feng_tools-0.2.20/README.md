# 铁锋的python工具箱

一个全面的Python工具包集合，提供了多种常用功能和工具函数。

## 项目简介

feng-tools 是一个综合性的Python工具库，集成了多个常用功能模块，旨在简化日常开发工作。该工具包涵盖了从文件操作到图像处理，从日志管理到AI应用等多个领域的实用工具。

## 环境要求

- Python >= 3.10

## 安装方法

```bash
pip install feng-tools
```

## 主要功能模块

### AI工具 (ai)
AI相关的工具和功能

### 文件操作 (file)
- TOML文件处理工具
- 文件读写操作

### HTTP工具 (http)
- MIME类型工具
- HTTP请求处理

### 图像处理 (image)
- 图像Base64转换
- 图像水印处理

### 日志工具 (log)
- 标准日志工具
- Loguru日志工具

### OpenCV工具 (opencv)
- 图像捕获工具
- 人脸检测
- OpenCV常用操作

### 操作系统工具 (os)
- 系统操作工具
- Shell命令工具
- 系统信息工具

### 其他工具模块
- 下载工具 (download)
- 加密工具 (encrypt)
- ID生成工具 (id)
- JSON处理 (json)
- PDF处理 (pdf)
- 随机数生成 (random)
- 等等...

## 使用示例

```python
# 导入工具包
from feng_tools import file
from feng_tools.media import image
from feng_tools.base import log

# 使用日志工具
logger = log.get_logger()
logger.info("这是一条日志信息")

# 使用图像工具
image.add_watermark("input.jpg", "output.jpg", "水印文字")

# 使用文件工具
config = file.read_toml("config.toml")
```

## 贡献指南

欢迎提交问题和功能需求！如果您想贡献代码：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 作者

编程Thinker (imchentiefeng@aliyun.com)

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详细信息
