# 🎬 Text-to-Media Generator

使用 AI 将文案转换为视频和图像的完整解决方案。支持 Runway 和 Leonardo AI APIs。

## ✨ 功能特性

- 🎥 **文本生成视频** - 使用 Runway AI 从文案生成高质量视频
- 🖼️ **文本生成图像** - 使用 Leonardo AI 从文案生成精美图像
- 🌐 **现代化Web UI** - 直观的用户界面，支持批量操作
- 📊 **生成历史** - 追踪所有生成的内容
- ⚙️ **灵活配置** - 自定义分辨率、时长、质量等参数
- 🚀 **快速部署** - Docker 和 Docker Compose 支持
- 🔄 **API 接口** - RESTful API 供第三方集成

## 📋 前置要求

- Python 3.8+
- Node.js 14+
- Runway API Key（[获取](https://runwayml.com)）
- Leonardo API Key（[获取](https://leonardo.ai)）
- Docker & Docker Compose（可选）

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/2984035940-lab/text-to-media-generator.git
cd text-to-media-generator
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```env
RUNWAY_API_KEY=your-runway-api-key
LEONARDO_API_KEY=your-leonardo-api-key
```

### 3. 本地运行

#### 后端（Python Flask）

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端将在 `http://localhost:5000` 运行

#### 前端（Node.js Express）

在另一个终端中：

```bash
cd frontend
npm install
npm start
```

前端将在 `http://localhost:3000` 运行

### 4. 使用 Docker Compose 运行

```bash
docker-compose up --build
```

然后访问 `http://localhost:3000`

## 📖 API 文档

### 生成视频

**端点**: `POST /api/generate-video`

**请求体**:
```json
{
  "prompt": "美丽的日落景色，云彩变化",
  "duration": 5,
  "fps": 24,
  "width": 1280,
  "height": 720
}
```

**响应**:
```json
{
  "task_id": "task_123456",
  "status": "pending",
  "video_url": "https://..."
}
```

### 生成图像

**端点**: `POST /api/generate-image`

**请求体**:
```json
{
  "prompt": "油画风格的山水画",
  "negative_prompt": "低质量、模糊",
  "num_images": 1,
  "width": 768,
  "height": 768,
  "guidance_scale": 7.5
}
```

**响应**:
```json
{
  "generation_id": "gen_123456",
  "status": "pending",
  "images": ["https://..."]
}
```

### 获取任务状态

**端点**: `GET /api/tasks/<task_id>`

**端点**: `GET /api/generations/<generation_id>`

## 📁 项目结构

```
text-to-media-generator/
├── backend/
│   ├── app.py                 # Flask 应用主文件
│   ├── config.py              # 配置管理
│   ├── runway_client.py        # Runway API 客户端
│   ├── leonardo_client.py      # Leonardo API 客户端
│   └── requirements.txt        # Python 依赖
├── frontend/
│   ├── server.js              # Express 服务器
│   ├── package.json           # Node 依赖
│   └── public/
│       ├── index.html         # 主页面
│       └── app.js             # 前端逻辑
├── .env.example               # 环境变量模板
├── docker-compose.yml         # Docker Compose 配置
└── README.md                  # 本文档
```

## 🔧 配置参数

### 视频生成参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | string | - | 视频描述（必需） |
| duration | int | 5 | 视频时长（秒） |
| fps | int | 24 | 帧率 |
| width | int | 1280 | 视频宽度 |
| height | int | 720 | 视频高度 |

### 图像生成参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | string | - | 图像描述（必需） |
| negative_prompt | string | - | 反向提示词 |
| num_images | int | 1 | 生成数量 |
| width | int | 768 | 图像宽度 |
| height | int | 768 | 图像高度 |
| guidance_scale | float | 7.5 | 引导强度 |

## 🛠️ 故障排查

### API 密钥无效

确保在 `.env` 文件中正确设置了有效的 API 密钥。

### 后端连接失败

检查后端服务是否在 `http://localhost:5000` 运行。

### Docker 构建失败

尝试清理并重新构建：
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## 📝 示例用例

### 使用 cURL 生成视频

```bash
curl -X POST http://localhost:5000/api/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "宁静的森林中的小溪，阳光透过树叶洒下",
    "duration": 10,
    "width": 1920,
    "height": 1080
  }'
```

### 使用 Python 生成图像

```python
import requests
import json

url = "http://localhost:5000/api/generate-image"
payload = {
    "prompt": "星空下的城市，霓虹灯闪烁",
    "num_images": 2,
    "guidance_scale": 8.5
}

response = requests.post(url, json=payload)
result = response.json()
print(json.dumps(result, indent=2))
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📧 联系方式

有问题或建议？欢迎通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至 support@example.com

## 🙏 致谢

感谢 Runway 和 Leonardo 提供的强大 AI 模型和 API 服务。

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**
