# 🎯 选课推荐系统

> 基于 Flask + Vue 3 + Element Plus 构建的智能选课平台，让选课更高效、更科学。

---

## 📋 目录

- [项目简介](#-项目简介)
- [技术栈](#-技术栈)
- [快速开始](#-快速开始)
- [功能总览](#-功能总览)
- [项目结构](#-项目结构)
- [部署指南](#-部署指南)
- [API 概览](#-api-概览)
- [性能优化](#-性能优化)

---

## 💡 项目简介

选课推荐系统是一个面向高校的课程管理与选课辅助平台，提供课程检索、教师评价、模拟选课、账户管理等一站式服务。系统采用前后端分离架构，支持多角色权限管理，兼顾桌面端与移动端体验。

**核心能力：**
- 📚 **课程管理** — 多维度课程检索与筛选，支持拼音缩写搜索教师
- ⭐ **教师评价** — 按老师分组评分，实时查看评价详情
- 🎮 **模拟选课** — 14 步完整选课流程，学分看板实时统计
- 👥 **多角色权限** — 超级管理员、管理员、学生三级权限体系
- 📱 **移动端适配** — 毛玻璃设计，侧滑菜单，响应式布局

---

## 🛠 技术栈

### 后端

| 类别 | 技术 | 用途 |
|------|------|------|
| 框架 | Flask 3.0 | Web 服务框架 |
| ORM | Flask-SQLAlchemy | 数据库 ORM |
| 认证 | Flask-JWT-Extended | JWT Token 认证 |
| 数据库 | MySQL 8.4 / SQLite | 生产 / 开发 |
| 缓存 | Redis 8.6 | 数据缓存加速 |
| WSGI | Gunicorn | 生产环境部署 |

### 前端

| 类别 | 技术 | 用途 |
|------|------|------|
| 框架 | Vue 3 | 前端 MVVM 框架 |
| UI | Element Plus | 企业级组件库 |
| 路由 | Vue Router 4 | 前端路由管理 |
| HTTP | Axios | API 请求封装 |
| 构建 | Vue CLI 5 | 项目构建打包 |

### 部署

| 类别 | 技术 |
|------|------|
| Web 服务器 | Nginx 1.30（反向代理 + 缓存 + Gzip） |
| 进程管理 | Systemd |
| 云平台 | 腾讯云轻量应用服务器（Ubuntu 24.04） |

---

## 🚀 快速开始

### 环境要求

| 组件 | 最低版本 | 推荐版本 | 说明 |
|------|---------|---------|------|
| Python | 3.8 | **3.12+** | 代码语法兼容 3.6+，Flask 3.0 要求 ≥3.8 |
| Node.js | 16 | **20+** | 前端构建环境 |
| npm | 8 | **10+** | 随 Node.js 版本自动匹配 |
| MySQL | 8.0 | **8.4** | 生产环境，认证插件 `caching_sha2_password` |
| SQLite | 3.x | 3.x | 开发环境，无需单独安装 |
| Redis | 7.0 | **8.6** | 缓存服务，基础命令全版本兼容 |

### 1. 启动后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 启动服务（默认 SQLite，自动建库）
python app.py
```

后端服务 → http://127.0.0.1:5001

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install --registry=https://registry.npmmirror.com

# 启动开发服务器
npm run serve
```

前端服务 → http://localhost:8080

### 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 学生 | student | student123 |

---

## ✨ 功能总览

### 👑 超级管理员

账户管理、课程管理、评价管理、注册审核、数据清空。

### 👤 管理员

- **双模式界面**：进入后默认学生模式，右上角一键切换管理面板
- **课程管理**：增删改查，支持多学期、多课程性质、分专业设置必修/选修
- **评价管理**：增删改查，支持课程名和教师搜索
- **教师搜索**：支持拼音缩写（如输入 `wls` 搜索"汪礼胜"）

### 🎓 学生

- **多维度课程检索**：
  - 搜索课程名
  - 按专业分类筛选
  - 按课程性质多选筛选
  - 按必修/选修筛选
  - 教师拼音缩写搜索
- **教师评价**：查看评分、添加/删除评价
- **模拟选课**：完整选课流程体验

### 🎮 模拟选课系统

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

**特色**：学分看板实时统计、体育先修检测、选课清单导出。

### 📱 移动端体验

- **毛玻璃设计**：半透明背景 + 模糊效果 + 圆角卡片
- **侧滑菜单**：从右滑入，包含所有导航入口
- **筛选面板**：点击"筛选"弹出，包含全部搜索条件
- **简化分页**：隐藏数字按钮，保留"第 m/n 页"跳转
- **两列卡片**：紧凑美观的课程卡片布局
- **骨架屏**：加载时显示动画占位

---

## 📁 项目结构

```
Select/
├── backend/                          # Flask 后端
│   ├── app.py                       # 主应用（路由、缓存、JWT）
│   ├── models.py                    # 数据模型
│   ├── config.py                    # 配置管理
│   ├── cache.py                     # Redis 缓存
│   ├── requirements.txt             # Python 依赖
│   ├── deploy/                      # 部署配置
│   │   ├── nginx.conf              # Nginx 配置
│   │   └── course-recommendation.service  # Systemd 服务
│   ├── tools/                       # 工具脚本
│   │   ├── init_db.py              # 数据库初始化
│   │   └── init_mysql_tables.py    # MySQL 建表
│   └── logs/                        # 日志目录
│
├── frontend/                         # Vue 前端
│   ├── dist/                        # 构建产物（上传到服务器）
│   ├── src/
│   │   ├── api/                     # API 封装
│   │   ├── router/                  # 路由配置
│   │   ├── views/                   # 页面组件
│   │   │   ├── Login.vue           # 登录页
│   │   │   ├── Register.vue        # 注册页
│   │   │   ├── StudentDashboard.vue # 学生端主页
│   │   │   ├── AdminDashboard.vue   # 管理端主页
│   │   │   ├── UserCenter.vue       # 用户中心
│   │   │   ├── UserManagement.vue   # 用户管理
│   │   │   ├── Feedback.vue         # 用户反馈
│   │   │   └── SimulatedSelection.vue # 模拟选课
│   │   ├── App.vue                  # 根组件
│   │   ├── style.css                # 全局样式
│   │   └── main.js                  # 入口文件
│   └── package.json
│
└── README.md
```

---

## 📦 部署指南

### 架构

```
用户 → Nginx (80) → Gunicorn (2 workers) → MySQL + Redis
         ├── 静态资源 → 直接返回（强缓存 1 年）[root: /home/ubuntu/course-recommendation/frontend/dist]
         └── /api/* → 反向代理到后端
```

### 部署步骤

```bash
# 1. 配置环境变量
cd backend
cp .env.example .env
# 编辑 .env，配置数据库连接

# 2. 安装依赖 & 初始化数据库
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE course_recommendation CHARACTER SET utf8mb4;"
python tools/init_mysql_tables.py

# 3. 构建前端
cd frontend
npm install
npm run build

# 4. 上传前端静态文件到服务器
scp -r dist/* ubuntu@<服务器IP>:/home/ubuntu/course-recommendation/frontend/dist/

# 5. 配置 Nginx
sudo cp backend/deploy/nginx.conf /etc/nginx/sites-available/course-recommendation
sudo ln -s /etc/nginx/sites-available/course-recommendation /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# 6. 配置 Systemd 服务
sudo cp backend/deploy/course-recommendation.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now course-recommendation
```

### Nginx 缓存策略

| 资源类型 | 缓存时间 | 策略 |
|---------|---------|------|
| JS/CSS/字体 | 1 年 | `public, immutable` |
| 图片 | 30 天 | `public, immutable` |
| index.html | 不缓存 | `no-cache` |
| API 请求 | 不缓存 | 反向代理 |

---

## 🔌 API 概览

| 模块 | 端点 | 说明 |
|------|------|------|
| 认证 | `/api/auth/*` | 登录、注册、Token 刷新 |
| 用户 | `/api/user/*` | 个人信息、密码修改、账号注销 |
| 课程 | `/api/courses/*` | 课程 CRUD、筛选、排序 |
| 教师 | `/api/teachers/*` | 教师列表、搜索 |
| 评价 | `/api/evaluations/*` | 评价 CRUD、评分统计 |
| 专业 | `/api/majors/*` | 专业列表 |
| 管理 | `/api/admin/*` | 用户管理、注册审核、数据清空 |
| 反馈 | `/api/feedback/*` | 反馈提交、回复 |

---

## ⚡ 性能优化

### 缓存策略

| 数据 | 缓存时间 | 失效时机 |
|------|---------|---------|
| 课程列表 | 5 分钟 | 增/删/改课程或评价 |
| 专业列表 | 1 小时 | 增/删/改专业 |
| 教师列表 | 1 小时 | 增/删/改教师 |

### 优化措施

- **Redis 缓存**：减少数据库查询
- **MySQL 连接池**：20 + 10 溢出连接
- **Nginx 静态缓存**：JS/CSS/图片直接返回
- **Gzip 压缩**：压缩级别 6
- **图片压缩**：背景图 1018KB → 105KB（90%）

---

## 📝 核心功能详解

### 课程序号
- 自定义序号排序，支持升序/降序
- 列表显示序号，隐藏数据库 ID

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

---

## 📄 许可

本项目仅供学习交流使用。
