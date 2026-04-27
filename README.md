# 选课推荐系统

一个基于 Flask + Vue 3 + Element Plus 的选课推荐系统，支持课程管理、教师评价、多维度筛选、模拟选课、账户管理等功能。

## 技术栈

### 后端
- **框架**: Flask 2.3 + Flask-SQLAlchemy + Flask-JWT-Extended + Flask-CORS
- **WSGI 服务器**: Gunicorn (生产) / Waitress (Windows 开发)
- **数据库**: MySQL 8.0 (生产) / SQLite (开发)
- **缓存**: Redis (生产环境)
- **ORM**: SQLAlchemy 连接池管理

### 前端
- **框架**: Vue 3 (Composition API)
- **UI 组件库**: Element Plus
- **路由**: Vue Router 4
- **HTTP 客户端**: Axios
- **构建工具**: Vue CLI 5

### 部署
- **Web 服务器**: Nginx (反向代理 + 静态资源缓存 + Gzip 压缩)
- **进程管理**: Systemd
- **云平台**: 腾讯云轻量应用服务器 (Ubuntu 22.04, 2核2G)

## 项目结构

```
Select/
├── backend/                    # Flask 后端
│   ├── app.py                 # 主应用文件（路由、缓存、JWT 认证）
│   ├── models.py              # 数据模型（User, Course, Teacher, Evaluation 等）
│   ├── config.py              # 配置（MySQL 连接池、Redis 缓存、JWT 等）
│   ├── cache.py               # Redis 缓存管理器
│   ├── requirements.txt       # Python 依赖
│   ├── .env.example           # 环境变量模板
│   ├── instance/              # SQLite 数据库目录（开发环境）
│   ├── deploy/                # 部署配置
│   │   ├── nginx.conf         # Nginx 配置（反向代理 + 缓存策略）
│   │   ├── course-recommendation.service  # Systemd 服务配置
│   │   ├── compress_images.py # 图片压缩脚本
│   │   ├── check_db.sh        # 数据库连接检查脚本
│   │   ├── check_mysql.sh     # MySQL 状态检查脚本
│   │   ├── check_sqlite.sh    # SQLite 状态检查脚本
│   │   ├── check_users.sh     # 用户数据检查脚本
│   │   └── check_images.py    # 图片资源检查脚本
│   ├── tools/                 # 辅助工具脚本
│   │   ├── init_db.py              # 数据库初始化
│   │   ├── init_mysql_tables.py    # MySQL 表初始化
│   │   ├── check_majors.py         # 专业数据检查
│   │   ├── check_academic_courses.py   # 学科课程检查
│   │   ├── check_english_courses.py    # 英语课程检查
│   │   ├── check_pe_courses.py         # 体育课程检查
│   │   ├── check_practice_courses.py   # 实践课程检查
│   │   ├── check_major_required.py     # 专业必修检查
│   │   └── check_general_elective.py   # 通识选修检查
│   └── logs/                  # Gunicorn 日志目录
├── frontend/                  # Vue 前端
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── api/               # API 调用封装
│   │   ├── views/             # 页面组件
│   │   │   ├── Login.vue      # 登录页（毛玻璃效果）
│   │   │   ├── Register.vue   # 注册页
│   │   │   ├── StudentDashboard.vue  # 学生端主页
│   │   │   ├── AdminDashboard.vue    # 管理端主页
│   │   │   ├── UserCenter.vue        # 用户中心
│   │   │   ├── UserManagement.vue    # 用户管理（超级管理员）
│   │   │   ├── Feedback.vue          # 用户反馈
│   │   │   └── SimulatedSelection.vue # 模拟选课
│   │   ├── router/            # 路由配置
│   │   ├── App.vue            # 根组件（全局样式 + 页面过渡动画）
│   │   └── main.js            # 入口文件
│   └── package.json           # Node 依赖
└── README.md
```

## 功能特性

### 超级管理员
- 登录认证（JWT Token，30天有效期）
- 所有管理员功能
- 账户管理
  - 查看所有账户列表（学号/姓名脱敏显示，支持解密查看）
  - 创建新账户（管理员/学生），需填写真实姓名和学号
  - 审核注册申请（通过/拒绝）
  - 修改用户角色
  - 删除账户
- 课程管理（添加、编辑、删除、查询）
- 评价管理（添加、编辑、删除、查询）
- 清空所有数据功能
- 唯一身份，不能更改自己的角色

### 管理员
- 登录认证（JWT Token，30天有效期）
- 初始进入界面与学生端一致，右上角可切换"管理面板"
- 课程管理（添加、编辑、删除、查询）
  - 支持多个开课学期（春季、秋季可同时选择）
  - 支持多个课程性质（通识必修、通识选修、个性课程、学科必修、专业必修、专业选修、实践课、英语必修、体育必修可同时选择）
  - 支持为不同专业设置不同的课程性质（必修/选修）
  - 课程性质筛选器，支持多选筛选
  - 教师搜索（支持拼音缩写）
- 教师评价管理（添加、编辑、删除、查询）
  - 支持课程名搜索和教师搜索（支持拼音缩写）
- 按专业分类筛选课程
- 自定义课程序号，支持按序号排序（升序/降序）
- 评分按老师分组显示，每位老师显示评价人数
- 可在主页查看课程详情并添加评价
- 清空所有数据功能
- 数据库只在首次启动时初始化（保留用户数据）

### 学生
- 登录认证（JWT Token，30天有效期）
- 课程检索（多维度筛选）
  - 搜索课程名
  - 按专业分类筛选
  - 按课程性质筛选（支持多选）
  - 选择专业后，可按该专业的必修/选修筛选
  - 按教师搜索（支持拼音缩写，如输入"wls"搜索"汪礼胜"）
- 查看课程详情
- 查看教师评价（按老师分组显示评分和评价人数）
- 添加教师评价
- 删除自己的评价
- 显示建议修读学期
- **模拟选课** — 分步完成完整选课流程

### 模拟选课（SimulatedSelection）
模拟选课系统提供完整的选课流程体验，共 14 个步骤：

| 步骤 | 名称 | 说明 |
|------|------|------|
| 1 | 选择专业 | 选择所属专业（计算机类、软件、软件（实验）、大数据、人工智能、人工智能（实验）） |
| 2 | 选择方向 | 计算机类需进一步选择分流方向（计算机、软件） |
| 3 | 选择班级 | 计算机/软件专业选择班级类型（普通班/卓越工程师） |
| 4 | 通识必修 | 选择通识必修课程，默认全选 |
| 5 | 英语快/慢班 | 选择英语快班或慢班 |
| 6 | 英语必修 | 快班：大学英语2+3 + 2门其他；慢班：大学英语1+2+3 + 1门其他。需修满8学分 |
| 7 | 体育必修 | 基础体育+基础体育2 + 2门其他（中级课程需先修对应初级），需修满4学分 |
| 8 | 学科必修 | 选择学科必修课程，默认全选 |
| 9 | 专业必修 | 按专业加载必修课程，默认全选 |
| 10 | 专业选修 | 按专业加载选修课程，默认不选，需达到各专业学分要求 |
| 11 | 实践课 | 按专业加载实践课程，默认全选 |
| 12 | 通识选修 | 需修满9学分，含国家安全教育必修、艺术审美类2学分、四史/创新创业各1门 |
| 13 | 个性课程 | 需修满6学分 |
| 14 | 选课总结 | 汇总所有已选课程，支持导出为文本文件 |

**特色功能**：
- 学分看板实时统计已选学分
- 专业选修学分要求：计算机 24.5、软件 20.5、大数据 22.5、人工智能 24.5、软件（实验）21
- 通识选修支持按主题类别筛选（四史类、艺术审美类、创新创业类）
- 体育中级课程自动检测先修关系
- 人工智能（实验）因培养方案未完整，选完学科必修后提示结束
- 选课总结支持导出为 `选课清单_专业名.txt`

### 注册功能
- 支持学生和管理员角色注册
- 注册需填写：用户名、密码、真实姓名、学号、申请角色
- 注册后需等待超级管理员审核

### 用户中心
- 修改个人信息（学号、真实姓名）
- 修改密码
- 注销账号（超级管理员不可注销）

### 用户反馈
- 学生可提交反馈和查看自己的反馈
- 管理员/超级管理员可查看所有反馈并回复

## 快速开始（开发环境）

### 1. 后端启动

```bash
cd backend

# 安装依赖（使用国内镜像源）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 启动服务（默认使用 SQLite，自动创建数据库）
python app.py
```

后端服务运行在 http://127.0.0.1:5001

### 2. 前端启动

```bash
cd frontend

# 安装依赖（使用国内镜像源）
npm install --registry=https://registry.npmmirror.com

# 启动开发服务器
npm run serve
```

前端服务运行在 http://localhost:8080

## 生产环境部署

### 架构图

```
用户 → Nginx (80端口) → Gunicorn (2 workers) → MySQL + Redis
         ├── 静态资源（JS/CSS/图片）→ 直接返回（强缓存）
         └── /api/* → 反向代理到后端
```

### 前置条件

- Ubuntu 22.04 服务器
- Python 3.10+
- MySQL 8.0
- Redis
- Nginx
- Node.js 16+

### 部署步骤

#### 1. 配置环境变量

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，配置数据库和 Redis 连接信息
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 初始化数据库

```bash
# 创建 MySQL 数据库
mysql -u root -p -e "CREATE DATABASE course_recommendation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 初始化表结构
python init_mysql_tables.py
```

#### 4. 构建前端

```bash
cd frontend
npm install
npm run build
```

#### 5. 配置 Nginx

将 `deploy/nginx.conf` 中的 `server_name` 和 `root` 路径修改为实际值，然后：

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/course-recommendation
sudo ln -s /etc/nginx/sites-available/course-recommendation /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. 配置 Systemd 服务

```bash
sudo cp deploy/course-recommendation.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable course-recommendation
sudo systemctl start course-recommendation
```

### Nginx 缓存策略

| 资源类型 | 缓存时间 | 策略 |
|---------|---------|------|
| JS/CSS/字体 | 1 年 | `public, immutable` |
| 图片 (JPG/PNG/WebP) | 30 天 | `public, immutable` |
| index.html | 不缓存 | `no-cache, must-revalidate` |
| API 请求 | 不缓存 | 反向代理到后端 |

### Gzip 压缩

启用 Gzip 压缩，压缩级别 6，覆盖 JS/CSS/JSON/XML/SVG 等常见 MIME 类型。

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 学生 | student | student123 |

## 核心功能说明

### 课程序号功能
- 添加课程时可设置自定义序号（默认为 0）
- 编辑课程时可修改序号
- 支持按序号升序/降序排列
- 课程列表中显示序号，隐藏数据库 ID

### 多课程性质
- 一个课程可同时拥有多个课程性质
- 支持的课程性质：通识必修、通识选修、个性课程、学科必修、专业必修、专业选修、实践课、英语必修、体育必修
- 添加/编辑课程时可多选
- 支持按课程性质多选筛选

### 多开课学期
- 一个课程可同时在春季和秋季开课
- 添加/编辑课程时可多选学期
- 课程列表显示所有开课学期

### 分专业课程性质
- 同一门课程对不同专业可设置不同的课程性质（必修/选修）
- 添加/编辑课程时可为每个专业单独设置
- 学生端选择专业后，显示该课程对该专业的性质

### 教师评分
- 评分按老师分组显示，不同老师的评分分开展示
- 每位老师显示评分（保留一位小数）和评价人数
- 学生添加评价时需要选择具体的老师
- 管理员也可在主页查看课程详情并添加评价
- 课程详情页显示所有老师的评分
- 评价管理页面支持课程名和教师搜索

### 数据脱敏
- 学号：保留前 3 位和后 2 位，中间用 `*` 代替
- 姓名：保留姓氏，名字用 `*` 代替
- 超级管理员可解密查看完整信息

### 时区设置
- 系统时间采用东八区（北京时间）
- 评价时间显示为本地时间

## 高并发架构

### 当前配置

| 组件 | 配置 | 并发能力 |
|------|------|---------|
| Nginx | 2 workers, 768 connections | ~1500 并发连接 |
| Gunicorn | 2 sync workers | 2 并行请求 |
| MySQL | 连接池 20 + 溢出 10 | ~30 并发查询 |
| Redis | 单实例 | ~50000 QPS |
| 静态资源 | Nginx 直接返回 + 强缓存 | ~1000+ QPS |

### 缓存策略

| 数据 | 缓存时间 | 失效时机 |
|------|---------|---------|
| 课程列表 | 5 分钟 | 增/删/改课程或评价时清除 |
| 专业列表 | 1 小时 | 增/删/改专业时清除 |
| 教师列表 | 1 小时 | 增/删/改教师时清除 |

### 性能优化

- **Redis 缓存**：减少数据库查询压力
- **MySQL 连接池**：复用连接，减少连接开销
- **Nginx 静态缓存**：JS/CSS/图片直接由 Nginx 返回
- **Gzip 压缩**：减少传输体积
- **图片压缩**：登录背景图 1018KB → 105KB（90% 压缩率）

## 移动端适配

- 支持手机端访问
- 响应式布局，适配不同屏幕尺寸（768px / 480px 断点）
- 毛玻璃（Glassmorphism）UI 设计
- 卡片渐入动画
- 骨架屏加载状态
- 页面切换过渡动画

## 专业分类

系统包含以下专业（初始化时自动创建，可手动添加）：
- 计算机
- 软件
- 软件（实验）
- 大数据
- 人工智能
- 人工智能（实验）
- 计算机类

## 课程性质

系统支持以下课程性质：
- 通识必修
- 通识选修
- 个性课程
- 学科必修
- 专业必修
- 专业选修
- 实践课
- 英语必修
- 体育必修
