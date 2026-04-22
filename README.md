# Luvoy — AI 驱动的大学生职业规划智能体

> 基于大语言模型（LLM）的智能职业规划平台，集简历解析、岗位画像、人岗匹配、职业图谱、规划报告于一体。

---

## 目录

- [项目简介](#项目简介)
- [核心功能](#核心功能)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
  - [环境准备](#环境准备)
  - [Docker 一键部署（推荐）](#docker-一键部署推荐)
  - [本地开发部署](#本地开发部署)
- [配置说明](#配置说明)
- [API 接口一览](#api-接口一览)
- [目录结构](#目录结构)

---

## 项目简介

Luvoy 是一个面向高校学生的 AI 职业规划系统。学生上传简历后，系统通过大语言模型自动解析个人信息与能力标签，结合岗位知识图谱进行智能人岗匹配，最终输出个性化职业发展报告。

---

## 核心功能

| 功能模块 | 说明 |
|---|---|
| **简历解析** | 支持 PDF / DOCX / TXT，自动提取技能、学历、经历等结构化信息 |
| **岗位画像** | LLM 对招聘数据进行分析，生成岗位能力画像与分类标签 |
| **人岗匹配** | 两阶段匹配：向量召回 → LLM 精排，支持集成学习与多目标优化 |
| **职业图谱** | 基于 NetworkX 构建岗位关系图谱，展示职业晋升与转换路径 |
| **规划报告** | LLM 生成 Markdown 格式个性化报告，支持二次润色与导出 |
| **多算法支持** | AHP 层次分析、贝叶斯优化、强化学习、MCTS 规划等高级算法可选 |
| **移动端支持** | 前端基于 Capacitor 可打包为 Android APK |

---

## 技术架构

```
┌─────────────────────────────────────────────────────┐
│                     前端 (Vue 3)                      │
│  Vue3 · Vite · Pinia · Vue Router · ECharts          │
│  Bootstrap 5 · Tailwind CSS · Capacitor (Android)    │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / REST API
┌──────────────────────▼──────────────────────────────┐
│                   后端 (Flask)                        │
│  Flask · SQLAlchemy · OpenAI SDK (兼容格式)           │
│  NetworkX · scikit-learn · NumPy / SciPy             │
│  PyPDF2 · pdfplumber · PyMuPDF · python-docx         │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
   SQLite 数据库              LLM API（OpenAI 兼容）
   (可换 PostgreSQL)         DeepSeek / 通义千问 / 智谱 等
```

---

## 快速开始

### 环境准备

- Docker + Docker Compose（推荐）
- 或本地安装 Python ≥ 3.10、Node.js ≥ 18

### Docker 一键部署（推荐）

**1. 克隆仓库**

```bash
git clone <repo-url>
cd Luvoy
```

**2. 配置环境变量**

复制并编辑 `.env` 文件：

```bash
cp .env.example .env   # 如无 example 文件，请参考下方配置说明手动创建
```

**3. 启动服务**

```bash
docker compose up -d
```

- 前端：http://localhost:80
- 后端 API：http://localhost:5000

### 本地开发部署

#### 后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置 .env（见下方配置说明）

# 启动开发服务器
python run_server.py
# 或
flask run --host=0.0.0.0 --port=5000
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 生产构建
npm run build
```

#### 打包 Android APK

```bash
cd frontend
npm run build:apk
```

---

## 配置说明

在项目根目录（与 `docker-compose.yml` 同级）创建 `.env` 文件：

```dotenv
# LLM 配置（OpenAI 兼容接口）
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096

# Flask
SECRET_KEY=your-secret-key

# 匹配算法
MATCHING_RECALL_TOP_K=20
MATCHING_RERANK_TOP_N=5

# 图算法
GRAPH_ALGORITHM=dijkstra
GRAPH_PAGERANK_DAMPING=0.85

# AHP 算法开关
AHP_ENABLED=true

# 多智能体
AGENT_MAX_RETRIES=2
AGENT_ENABLE_COT=true
```

支持的 LLM 服务商（只需修改 `LLM_BASE_URL` 与 `LLM_MODEL`）：

| 服务商 | BASE_URL | 示例模型 |
|---|---|---|
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-max` |
| 智谱 AI | `https://open.bigmodel.cn/api/paas/v4` | `glm-4` |
| Moonshot | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o` |

---

## API 接口一览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/stats` | 系统概览统计 |
| GET | `/api/jobs` | 岗位列表（分页/搜索） |
| GET | `/api/jobs/:id` | 岗位详情 |
| GET | `/api/jobs/profiles` | 岗位画像列表 |
| POST | `/api/jobs/analyze` | 批量生成岗位画像 |
| GET | `/api/graph/data` | 职业图谱数据 |
| POST | `/api/graph/build` | 构建职业图谱 |
| GET | `/api/students` | 学生列表 |
| POST | `/api/students` | 创建学生（支持文件上传） |
| GET | `/api/students/:id` | 学生详情 |
| DELETE | `/api/students/:id` | 删除学生 |
| POST | `/api/students/:id/generate-profile` | 生成学生画像 |
| GET | `/api/matching/:sid` | 获取匹配结果 |
| POST | `/api/matching/:sid/run` | 执行人岗匹配 |
| GET | `/api/reports/:sid` | 获取职业规划报告 |
| POST | `/api/reports/:sid/generate` | 生成职业规划报告 |
| POST | `/api/reports/:rid/polish` | LLM 润色报告 |

---

## 目录结构

```
Luvoy/
├── docker-compose.yml          # 一键启动配置
├── .env                        # 环境变量（自行创建）
├── backend/
│   ├── app.py                  # Flask 应用入口 & 路由
│   ├── config.py               # 配置管理
│   ├── requirements.txt        # Python 依赖
│   ├── models/                 # 数据库模型（Student / Job / Report）
│   ├── services/               # 业务服务层
│   │   ├── llm_client.py       # LLM 调用封装
│   │   ├── resume_parser.py    # 简历解析
│   │   ├── matching_engine.py  # 人岗匹配引擎
│   │   ├── job_analyzer.py     # 岗位分析
│   │   ├── job_graph.py        # 职业图谱
│   │   ├── report_generator.py # 报告生成
│   │   └── algorithms/         # 高级算法（AHP/贝叶斯/RL/MCTS 等）
│   └── prompts/                # LLM Prompt 模板
└── frontend/
    ├── src/
    │   ├── views/              # 页面视图
    │   ├── components/         # 通用组件
    │   ├── stores/             # Pinia 状态管理
    │   ├── api/                # API 请求封装
    │   └── router/             # 路由配置
    └── android/                # Capacitor Android 工程
```

---

## License

MIT
