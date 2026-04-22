# Luvoy 部署指南

## 📦 本地开发使用

### 后端 (Flask)
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
python app.py               # 启动开发服务器 http://localhost:5000
```

### 前端 (Vue3 + Vite)
```bash
cd frontend
npm install
npm run dev                 # 启动开发服务器 http://localhost:5173
```

---

## 🐳 Docker 构建与推送

### 1. 登录 DockerHub
```bash
docker login
# 输入用户名和密码
```

### 2. 构建镜像
```bash
# 在项目根目录执行
cd E:\Luvoy

# 构建后端镜像
docker build -t maile123/luvoy-backend:latest ./backend

# 构建前端镜像
docker build -t maile123/luvoy-frontend:latest ./frontend
```

### 3. 推送到 DockerHub
```bash
docker push maile123/luvoy-backend:latest
docker push maile123/luvoy-frontend:latest
```

### 一键构建并推送 (使用 docker-compose)
```bash
# 构建
docker-compose build

# 推送
docker-compose push
```

---

## 🚀 服务器部署

### 1. 准备服务器
确保服务器已安装：
- Docker
- Docker Compose

### 2. 创建部署目录
```bash
mkdir -p /opt/luvoy
cd /opt/luvoy
```

### 3. 上传部署文件
将以下文件上传到服务器 `/opt/luvoy/`:
- `docker-compose.yml` (来自 deploy/ 目录)
- `.env` (基于 `.env.example` 修改)
- `jobs.json` (岗位数据文件)

### 4. 配置环境变量
```bash
cp .env.example .env
nano .env   # 编辑填入实际的 API Key
```

`.env` 文件内容：
```
LLM_API_KEY=sk-your-actual-api-key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
```

### 5. 拉取镜像并启动
```bash
docker-compose pull
docker-compose up -d
```

### 6. 查看日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 只看后端日志
docker-compose logs -f backend
```

### 7. 停止服务
```bash
docker-compose down
```

---

## 🔧 常用命令

```bash
# 查看运行状态
docker-compose ps

# 重启服务
docker-compose restart

# 更新镜像并重启
docker-compose pull && docker-compose up -d

# 进入后端容器调试
docker exec -it luvoy-backend bash

# 查看数据卷
docker volume ls
```

---

## 🌐 访问地址

| 服务 | 地址 |
|------|------|
| 前端界面 | http://服务器IP:80 |
| 后端 API | http://服务器IP:5000 |
| API 文档 | http://服务器IP:5000/api/stats |

---

## 📋 端口说明

| 端口 | 服务 | 说明 |
|------|------|------|
| 80 | Nginx | 前端静态文件 |
| 5000 | Gunicorn | 后端 API |

如需修改端口，编辑 `docker-compose.yml` 中的 `ports` 映射。
