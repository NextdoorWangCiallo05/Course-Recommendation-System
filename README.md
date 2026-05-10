# 选课推荐系统

基于 Flask + Vue 3 + Element Plus 构建的选课推荐系统，让选课更高效、更科学。

---

## 目录

- [项目简介](#-项目简介)
- [技术栈](#-技术栈)
- [快速开始](#-快速开始)
- [功能总览](#-功能总览)
- [项目结构](#-项目结构)
- [Docker 部署](#-docker-部署)
- [传统部署](#-传统部署)
- [API 概览](#-api-概览)
- [性能优化](#-性能优化)

---

## 项目简介

选课推荐系统是一个面向高校的课程管理与选课辅助平台，提供课程检索、教师评价、模拟选课、数据分析、账户管理等一站式服务。系统采用前后端分离架构，支持多角色权限管理，兼顾桌面端与移动端体验。

**核心能力：**
- **课程管理** — 多维度课程检索与筛选，支持拼音缩写搜索教师
- **教师评价** — 按老师分组评分，实时查看评价详情
- **模拟选课** — 14 步完整选课流程，学分看板实时统计
- **数据分析** — 教师评分排行、课程性质分布、各专业课程数量可视化
- **多角色权限** — 超级管理员、管理员、学生三级权限体系
- **深色模式** — 全局深色主题，毛玻璃设计，响应式布局

---

## 技术栈

### 后端

| 类别 | 技术 | 用途 |
|------|------|------|
| 框架 | Flask 3.0 | Web 服务框架 |
| ORM | Flask-SQLAlchemy | 数据库 ORM |
| 认证 | Flask-JWT-Extended | JWT Token 认证 |
| 限流 | Flask-Limiter | 接口速率限制 |
| 数据库 | MySQL 8.4 / SQLite | 生产 / 开发 |
| 缓存 | Redis 7 | 数据缓存加速 |
| WSGI | Gunicorn | 生产环境部署 |
| 日志 | 标准 logging | 文件 + 控制台日志 |

### 前端

| 类别 | 技术 | 用途 |
|------|------|------|
| 框架 | Vue 3 | 前端 MVVM 框架 |
| UI | Element Plus | 企业级组件库 |
| 图表 | ECharts | 数据分析可视化 |
| 路由 | Vue Router 4 | 前端路由管理 |
| HTTP | Axios | API 请求封装 |
| 构建 | Vue CLI 5 | 项目构建打包 |

### 部署

| 类别 | 技术 |
|------|------|
| Web 服务器 | Nginx（反向代理 + 静态缓存 + Gzip） |
| 进程管理 | Systemd / Docker Compose |
| 云平台 | 腾讯云轻量应用服务器（Ubuntu 24.04） |

---

## 快速开始

### 环境要求

#### 开发模式（SQLite）

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | ≥ 3.8 | Flask 3.0 要求，实测 3.12 - 3.14 均可 |
| Node.js | ≥ 18 | Vue CLI 5 构建要求，推荐 20 LTS / 22 LTS |
| npm | ≥ 8 | 随 Node.js 自带 |
| SQLite | 内置 | 开发模式无需单独安装 |

> 开发模式**不需要** MySQL、Redis、Docker，缓存自动降级不报错。

#### Docker 部署（生产环境）

| 组件 | 版本 | 说明 |
|------|------|------|
| Docker | ≥ 24 | 容器运行时 |
| Docker Compose | ≥ 2.24 | 容器编排（新版 Docker 内置） |
| Python | ≥ 3.8 | 后端运行在容器内 |
| Node.js | ≥ 18 | 前端构建在容器内 |
| MySQL | 8.4 | 运行在容器内 |
| Redis | 7.x | 运行在容器内 |

> 腾讯云服务器无法直连 Docker Hub 时，需在 `/etc/docker/daemon.json` 配置镜像加速：
> ```json
> {"registry-mirrors": ["https://mirror.ccs.tencentyun.com"]}
> ```

快速开始分两种方式：**开发模式**（SQLite，无需 Docker，最快体验）和 **Docker 部署**（MySQL + Redis，生产环境）。

---

### 方式一：开发模式（SQLite，无需 Docker）

无需安装 MySQL/Redis，零配置启动。

#### 1. 配置后端环境变量

```bash
cd backend
cp .env.example .env
# 开发模式直接使用默认值即可，生产环境时再替换密钥
```

#### 2. 启动后端

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

python app.py
```

首次启动会自动创建 SQLite 数据库和基础数据，控制台输出如下即成功：

```
INFO  数据库为空，正在初始化...
INFO  数据库初始化完成！（包含用户和基本专业）
INFO  启动开发服务器...
```

后端服务 → http://127.0.0.1:5001

#### 3. 启动前端

```bash
cd frontend

npm install --registry=https://registry.npmmirror.com

npm run serve
```

前端服务 → http://localhost:8080

---

### 方式二：Docker 部署（MySQL + Redis）

需要安装 Docker 和 Docker Compose。

#### 1. 配置环境变量

```bash
cp .env.example .env
# 生产环境建议重新生成密钥：
#   python -c "import secrets; print(secrets.token_hex(32))"
# 将输出的两个密钥分别填入 .env 的 SECRET_KEY 和 JWT_SECRET_KEY
```

#### 2. 一键启动

```bash
docker compose up -d
```

首次启动会自动拉取镜像、构建前后端、初始化数据库（耗时约 3-5 分钟）。

#### 3. 查看状态

```bash
docker compose ps          # 查看所有容器状态
docker compose logs -f backend   # 持续查看后端日志
```

#### 4. 导入已有数据（可选）

若宿主机 MySQL 已有数据，导出后导入 Docker MySQL：

```bash
# 宿主机导出
sudo mysqldump -u root course_recommendation > old_data.sql

# 导入 Docker MySQL
docker compose exec -T mysql mysql -u root -pRootPass2026! course_recommendation < old_data.sql
```

前端服务 → http://localhost

---

### 默认账号

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | admin | admin123 | 课程管理、评价管理 |
| 学生 | student | student123 | 检索课程、评价教师、模拟选课 |

---

## 功能总览

### 超级管理员

账户管理、课程管理、评价管理、注册审核、数据清空、通知中心。

### 管理员

- **双模式界面**：默认学生模式，右上角一键切换管理面板
- **课程管理**：增删改查，支持多学期、多课程性质、分专业设置必修/选修
- **评价管理**：增删改查，支持课程名和教师搜索
- **教师搜索**：支持拼音缩写（如输入 `wls` 搜索"汪礼胜"）
- **设置**：深色模式切换

### 学生

- **多维度课程检索**：
  - 搜索课程名
  - 按专业分类筛选
  - 按课程性质多选筛选
  - 按必修/选修筛选
  - 教师拼音缩写搜索
- **教师评价**：查看评分、添加/删除评价
- **模拟选课**：完整 14 步选课流程体验
- **数据分析**：教师评分排行、课程性质分布、各专业课程数量
- **设置**：深色模式切换

### 数据分析面板

| 图表 | 说明 |
|------|------|
| 教师评分排行 | 横向柱状图，可滚动查看全部教师 |
| 课程性质分布 | 饼图展示各类课程性质占比 |
| 各专业课程数量 | 柱状图展示各专业课程数量 |

### 模拟选课系统

14 步完成完整选课流程：

| 步骤 | 内容 | 说明 |
|------|------|------|
| 1-3 | 专业选择 | 选择专业、方向、班级 |
| 4 | 通识必修 | 默认全选 |
| 5-6 | 英语课程 | 快/慢班选择，需修满 8 学分 |
| 7 | 体育课程 | 基础体育 + 选修，需修满 4 学分 |
| 8-9 | 学科/专业必修 | 按专业加载，默认全选 |
| 10 | 专业选修 | 按专业加载，需达到学分要求 |
| 11 | 实践课 | 按专业加载，默认全选 |
| 12 | 通识选修 | 需修满 9 学分 |
| 13 | 个性课程 | 需修满 6 学分 |
| 14 | 选课总结 | 汇总导出为文本文件 |

### 移动端体验

- **毛玻璃设计**：半透明背景 + 模糊效果 + 圆角卡片
- **侧滑菜单**：从右滑入，包含所有导航入口
- **筛选面板**：点击"筛选"弹出，包含全部搜索条件
- **两列卡片**：紧凑美观的课程卡片布局
- **骨架屏**：加载时显示动画占位
- **深色模式**：跟随系统切换，界面自动适配

---

## 项目结构

```
Select/
├── backend/                          # Flask 后端
│   ├── app.py                       # 主应用（路由、JWT、限流、日志）
│   ├── models.py                    # 数据模型（User/Course/Teacher/Evaluation 等）
│   ├── config.py                    # 配置管理（数据库、Redis、缓存策略）
│   ├── cache.py                     # Redis 缓存管理器
│   ├── requirements.txt             # Python 依赖
│   ├── Dockerfile                   # Docker 构建文件
│   ├── entrypoint.sh                # 容器启动脚本（等待 MySQL + 初始化）
│   ├── gunicorn.conf.py             # Gunicorn 配置
│   ├── .env.example                 # 环境变量模板
│   └── deploy/                      # 部署配置
│       ├── nginx.conf              # Nginx 反向代理配置
│       └── course-recommendation.service  # Systemd 服务
│
├── frontend/                         # Vue 前端
│   ├── dist/                        # 构建产物
│   ├── src/
│   │   ├── api/                     # Axios API 封装
│   │   ├── router/                  # 路由配置
│   │   ├── views/
│   │   │   ├── Login.vue           # 登录页
│   │   │   ├── Register.vue        # 注册页
│   │   │   ├── StudentDashboard.vue # 学生端主页
│   │   │   ├── AdminDashboard.vue   # 管理端主页
│   │   │   ├── DataAnalysis.vue     # 数据分析
│   │   │   ├── SimulatedSelection.vue # 模拟选课
│   │   │   ├── Feedback.vue         # 意见反馈
│   │   │   ├── UserCenter.vue       # 用户中心
│   │   │   └── UserManagement.vue   # 用户管理
│   │   ├── App.vue                  # 根组件（全局样式、深色模式）
│   │   ├── style.css                # 全局样式
│   │   ├── main.js                  # 入口文件
│   │   └── constants.js             # 常量定义
│   ├── public/
│   │   ├── images/                  # 静态图片
│   │   └── index.html
│   ├── Dockerfile                   # 多阶段构建（Node + Nginx）
│   ├── deploy/nginx.conf            # Docker Nginx 配置
│   └── package.json
│
├── mysql/                           # MySQL 初始化
│   └── init/
│       └── 01_create_db.sql        # 建库建用户脚本
│
├── docker-compose.yml               # Docker Compose 编排（无 version，符合新规范）
├── .env                             # 生产环境密钥配置
└── README.md
```

---

## Docker 部署

### 一键启动

```bash
docker compose up -d
```

> 首次构建后端镜像时，Dockerfile 已配置清华源加速 apt 和 pip，无需手动配置。

### 服务架构

```
用户 → :80 ──► frontend (Nginx 静态文件)
               │
               └── /api/ → backend:5001 (Gunicorn/Flask, 内网)
                               ├── mysql:3306 (MySQL 8.4, 内网)
                               └── redis:6379 (Redis 7, 内网)
```

### 服务说明

| 服务 | 映射端口 | 说明 |
|------|---------|------|
| frontend | 宿主机 `:80` → 容器 `:80` | Nginx 静态文件服务 |
| backend | 不暴露宿主机（仅内网） | Gunicorn + Flask API |
| mysql | 宿主机 `127.0.0.1:3307` → 容器 `:3306` | MySQL 8.4 数据库 |
| redis | 宿主机 `127.0.0.1:6379` → 容器 `:6379` | Redis 7 缓存 |

> backend 不暴露宿主机端口，Nginx 通过 Docker 内部 DNS 直接访问 `backend:5001`，避免端口冲突。

### 数据持久化

- MySQL 数据 → 命名卷 `mysql_data`
- Redis 数据 → 命名卷 `redis_data`
- 后端日志 → 命名卷 `backend_logs`

---

## 传统部署

### 架构

```
用户 → Nginx (80) → Gunicorn (4 workers) → MySQL + Redis
         ├── 静态资源 → 直接返回（强缓存 1 年）
         └── /api/* → 反向代理到后端
```

### 部署步骤

```bash
# 1. 配置环境变量
cp backend/.env.example backend/.env

# 2. 安装后端依赖
cd backend
pip install -r requirements.txt

# 3. 创建 MySQL 数据库
mysql -u root -p -e "CREATE DATABASE course_recommendation CHARACTER SET utf8mb4;"

# 4. 构建前端
cd frontend
npm install
npm run build

# 5. 配置 Nginx
sudo cp backend/deploy/nginx.conf /etc/nginx/sites-available/course-recommendation
sudo ln -s /etc/nginx/sites-available/course-recommendation /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# 6. 配置 Systemd 服务
sudo cp backend/deploy/course-recommendation.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now course-recommendation
```

---

## API 概览

| 模块 | 端点 | 说明 |
|------|------|------|
| 认证 | `POST /api/login` | 登录（返回 JWT Token） |
| 认证 | `POST /api/register` | 注册（限流 3 次/小时） |
| 用户 | `GET /api/users` | 用户列表（超级管理员） |
| 课程 | `GET /api/courses` | 课程检索与筛选 |
| 课程 | `POST /api/courses` | 新增课程 |
| 课程 | `PUT /api/courses/<id>` | 更新课程 |
| 课程 | `DELETE /api/courses/<id>` | 删除课程 |
| 教师 | `GET /api/teachers` | 教师列表与搜索 |
| 评价 | `GET /api/evaluations` | 评价列表 |
| 评价 | `POST /api/evaluations` | 添加评价 |
| 评价 | `DELETE /api/evaluations/<id>` | 删除评价 |
| 专业 | `GET /api/majors` | 专业列表 |
| 数据分析 | `GET /api/stats/teacher-ratings` | 教师评分排行 |
| 数据分析 | `GET /api/stats/course-type-distribution` | 课程性质分布 |
| 数据分析 | `GET /api/stats/major-course-counts` | 各专业课程数量 |
| 通知 | `GET /api/notifications/pending-users` | 待审核用户（超级管理员） |
| 反馈 | `POST /api/feedback` | 提交反馈 |
| 反馈 | `GET /api/feedback` | 反馈列表 |

---

## 性能优化

### 缓存策略

| 数据 | 缓存时间 | 失效时机 |
|------|---------|---------|
| 课程列表 | 5 分钟 | 增/删/改课程或评价 |
| 专业列表 | 1 小时 | 增/删/改专业 |
| 教师列表 | 1 小时 | 增/删/改教师 |

### Nginx 缓存策略

| 资源类型 | 缓存时间 | 策略 |
|---------|---------|------|
| JS/CSS/字体 | 1 年 | `public, immutable` |
| 图片 | 30 天 | `public, immutable` |
| index.html | 不缓存 | `no-cache` |

### 优化措施

- **Redis 缓存**：减少数据库查询
- **MySQL 连接池**：20 + 10 溢出连接，自动回收
- **Nginx 静态缓存**：JS/CSS/图片直接返回
- **Gzip 压缩**：压缩级别 6
- **接口限流**：默认 200 次/小时，注册接口 3 次/小时

---

## 核心功能详解

### 多课程性质
- 一门课可同时属于多个性质（通识必修、专业选修等）
- 支持多选筛选

### 分专业课程性质
- 同一课程对不同专业可设置不同性质（必修/选修）
- 学生选择专业后自动适配

### 教师评分
- 按老师分组显示评分和评价人数
- 评分保留一位小数
- 支持课程名和教师搜索

### 数据脱敏
- 学号：保留前 3 位 + 后 2 位，中间 `***`
- 姓名：保留姓氏，名字 `*`
- 超级管理员可解密查看

### 安全措施
- 密码长度至少 8 位，必须包含字母和数字
- 用户名只能包含字母、数字和下划线
- 注册接口限流 3 次/小时
- 密码使用 Werkzeug 哈希存储
- JWT Token 24 小时过期
- 请求日志记录所有 API 调用
