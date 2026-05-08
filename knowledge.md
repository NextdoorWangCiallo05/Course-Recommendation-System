# 课程推荐系统 — 基础知识清单

> 本文档按学科分类，列出开发本课程推荐系统所涉及的基础知识，供复习和参考。

---

## 一、前端基础

### 1.1 HTML / CSS

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| HTML 语义化标签 | header、main、footer 等语义标签 | 页面结构布局 |
| CSS 选择器 | 类选择器、属性选择器、伪类、伪元素 | 组件样式控制 |
| CSS 盒模型 | margin、padding、border、content | 元素间距与布局 |
| Flex 布局 | display: flex、justify-content、align-items | 顶栏、卡片、筛选栏布局 |
| CSS 定位 | position: fixed / sticky / absolute / relative | 顶栏固定、毛玻璃面板定位 |
| CSS 过渡与动画 | transition、@keyframes、animation | 骨架屏闪烁、页面切换动画 |
| 媒体查询 | @media (max-width: 768px) | 移动端响应式适配 |
| 毛玻璃效果 | backdrop-filter: blur()、background: rgba() | 登录页、卡片、面板背景 |
| CSS 变量 | --primary-color 等自定义属性 | 统一主题色管理 |
| 渐变背景 | linear-gradient、radial-gradient | 按钮、刷新按钮渐变 |

### 1.2 JavaScript

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| ES6 语法 | let/const、箭头函数、模板字符串、解构赋值 | 全项目通用 |
| Promise / async-await | 异步编程 | API 请求、数据加载 |
| 数组方法 | map、filter、find、forEach、some | 课程筛选、数据转换 |
| 防抖（Debounce） | setTimeout + clearTimeout 模式 | 搜索输入防抖 |
| 事件处理 | click、input、change 事件 | 按钮点击、搜索输入、分页切换 |
| localStorage | 浏览器本地存储 | Token 持久化存储 |
| 正则表达式 | 字符串匹配与替换 | 拼音缩写搜索 |

### 1.3 Vue.js 框架

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| Vue 实例 / data / methods | 组件数据与方法定义 | 所有页面组件 |
| 模板语法 | {{ }} 插值、v-bind、v-on、v-model | 数据绑定、事件绑定、表单输入 |
| 条件渲染 | v-if / v-else / v-show | 加载状态、空数据提示、角色切换 |
| 列表渲染 | v-for + :key | 课程列表、评价列表、分页 |
| 计算属性 | computed | 筛选后的课程列表、分页数据 |
| 侦听器 | watch | 搜索条件变化触发筛选 |
| 组件通信 | props、$emit | 父子组件数据传递 |
| 生命周期 | mounted、created、beforeDestroy | 页面初始化加载数据 |
| 混入（mixin） | 复用组件逻辑 | 搜索防抖逻辑复用 |
| 作用域插槽 | slot-scope | 表格自定义列渲染 |
| 动态组件 | <component :is=""> | 管理员/学生模式切换 |
| 过渡动画 | <transition> 组件 | 页面切换、面板弹出动画 |
| 路由 | vue-router | 页面导航、路由守卫 |
| 导航守卫 | router.beforeEach | 登录鉴权、页面访问控制 |

### 1.4 Element Plus 组件库

| 组件 | 说明 | 在本项目中的应用 |
|------|------|------------------|
| el-header / el-main | 布局容器 | 页面整体布局 |
| el-card | 卡片容器 | 课程展示卡片 |
| el-table / el-table-column | 表格 | 管理员课程列表、评价列表 |
| el-pagination | 分页 | 课程列表分页 |
| el-input | 输入框 | 搜索框、表单输入 |
| el-select / el-option | 下拉选择器 | 专业筛选、课程性质筛选 |
| el-tag | 标签 | 课程性质标签、必修/选修标识 |
| el-button | 按钮 | 操作按钮、提交按钮 |
| el-dialog | 对话框 | 课程详情、添加评价、编辑课程 |
| el-form / el-form-item | 表单 | 登录、注册、编辑课程表单 |
| el-descriptions | 描述列表 | 课程详情展示 |
| el-empty | 空状态 | 无数据提示 |
| el-tabs / el-tab-pane | 标签页 | 管理员面板切换 |
| el-row / el-col | 栅格布局 | 响应式布局 |
| el-menu | 菜单 | 管理员侧边栏 |
| el-switch | 开关 | 管理员/学生模式切换 |
| el-rate | 评分 | 教师评分显示 |
| el-input-number | 数字输入框 | 学分输入 |
| el-color-picker | 颜色选择器 | 课程标签颜色 |
| el-tooltip | 提示 | 操作按钮提示 |
| el-popconfirm | 确认弹窗 | 删除确认 |
| el-badge | 徽标 | 未读反馈数量 |
| el-skeleton | 骨架屏 | 加载占位 |

---

## 二、后端基础

### 2.1 Python

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| Python 基础语法 | 变量、类型、函数、类 | 全项目通用 |
| 装饰器 | @app.route、@jwt_required | 路由注册、权限控制 |
| 上下文管理器 | with 语句 | 数据库连接管理 |
| 生成器 | yield | 分页查询 |
| 类型提示 | typing 模块 | 函数签名、代码可读性 |
| 日期时间处理 | datetime 模块 | 选课学期判断、时间戳 |
| 正则表达式 | re 模块 | 拼音缩写匹配 |
| 文件操作 | open、json 模块 | 数据导出、配置文件读取 |

### 2.2 Flask Web 框架

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 路由注册 | @app.route()、Blueprint | API 接口定义 |
| 请求处理 | request.json、request.args | 获取请求参数 |
| 响应处理 | jsonify()、Response | 返回 JSON 数据 |
| 错误处理 | @app.errorhandler | 统一异常处理 |
| 请求钩子 | before_request、after_request | CORS 跨域处理 |
| 会话管理 | session | 用户会话（配合 JWT） |
| 应用工厂 | create_app() | 应用初始化 |

### 2.3 SQLAlchemy ORM

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 模型定义 | db.Model、Column、关系定义 | User、Course、Teacher 等模型 |
| 字段类型 | String、Integer、Float、Text、DateTime | 模型字段定义 |
| 关系映射 | relationship、backref、foreign key | 课程-教师、评价-用户关联 |
| 查询 API | query、filter、order_by、limit/offset | 数据查询与分页 |
| 聚合查询 | func.count、func.avg | 评分统计、评价人数统计 |
| 多表联查 | join、outerjoin | 课程+教师+评价联合查询 |
| 事务管理 | db.session.commit / rollback | 数据写入一致性 |
| 迁移 | Flask-Migrate（Alembic） | 数据库表结构变更 |

### 2.4 JWT 认证

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| Token 生成 | jwt.encode() | 登录成功后签发 Token |
| Token 验证 | jwt.decode()、@jwt_required | 接口鉴权 |
| Token 过期 | exp 声明 | 30 天有效期 |
| 负载信息 | sub、role 等自定义声明 | 用户身份识别 |

### 2.5 Redis 缓存

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 缓存策略 | 缓存穿透、缓存雪崩 | 课程列表缓存 |
| 缓存过期 | EXPIRE、TTL | 5 分钟 / 1 小时缓存 |
| 缓存失效 | 主动删除（DEL） | 数据变更后清除缓存 |
| 序列化 | JSON 序列化/反序列化 | 复杂数据缓存 |

### 2.6 MySQL / SQLite

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 数据库设计 | 表结构设计、ER 图 | 9 张数据表 |
| 索引优化 | 联合索引、覆盖索引 | 课程名、专业、教师搜索加速 |
| 连接池 | 连接复用、最大连接数 | 高并发下数据库连接管理 |
| 事务隔离 | 读已提交 | 选课数据一致性 |
| SQL 函数 | LIKE、GROUP BY、HAVING | 模糊搜索、分组统计 |

---

## 三、部署与运维

### 3.1 Linux

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 基本命令 | ls、cd、cp、mv、rm、vim | 服务器文件管理 |
| 权限管理 | chmod、chown、useradd | 服务运行用户配置 |
| 进程管理 | systemctl、ps、kill | 服务启停与监控 |
| 日志查看 | journalctl、tail -f | 服务日志排查 |
| 防火墙 | ufw、iptables | 端口开放控制 |

### 3.2 Nginx

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 反向代理 | proxy_pass | 前端请求转发到 Flask |
| 静态文件服务 | root、try_files | 前端 SPA 静态资源 |
| Gzip 压缩 | gzip on | 传输压缩 |
| 缓存策略 | expires、Cache-Control | 静态资源缓存 |
| SSL/TLS | HTTPS 证书配置 | 安全通信 |
| 负载均衡 | upstream | 多实例部署 |

### 3.3 Gunicorn

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| WSGI 服务器 | Gunicorn 启动 Flask | 生产环境 Python Web 服务 |
| 工作模式 | sync、gevent | 并发处理 |
| 进程管理 | workers、threads | 多进程配置 |
| 日志配置 | accesslog、errorlog | 请求日志与错误日志 |

---

## 四、开发工具

### 4.1 Git

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 基本操作 | add、commit、push、pull | 版本管理 |
| 分支管理 | branch、merge、rebase | 功能分支开发 |
| 冲突解决 | merge conflict | 多人协作 |
| .gitignore | 忽略规则 | 排除 node_modules、dist、.env |

### 4.2 npm / Node.js

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 包管理 | npm install、package.json | 前端依赖管理 |
| 构建脚本 | npm run build、npm run serve | 开发与构建 |
| Vue CLI | vue create、vue.config.js | 项目脚手架 |

### 4.3 pip / Python 包管理

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 虚拟环境 | venv、virtualenv | 隔离 Python 依赖 |
| 依赖管理 | pip install、requirements.txt | 后端依赖安装 |
| 镜像源 | 清华、阿里云 PyPI 镜像 | 加速依赖下载 |

---

## 五、计算机基础

### 5.1 计算机网络

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| HTTP 协议 | 请求方法、状态码、请求头 | 前后端 API 通信 |
| RESTful API | GET/POST/PUT/DELETE 语义 | 接口设计规范 |
| CORS 跨域 | 同源策略、跨域请求 | 前后端分离部署 |
| TCP/IP | 三次握手、四次挥手 | 网络通信基础 |
| DNS | 域名解析 | 服务器域名配置 |

### 5.2 数据结构

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 数组 / 列表 | 有序集合 | 课程列表、评价列表 |
| 哈希表 / 字典 | 键值对存储 | 缓存、配置、请求参数 |
| 集合 | 去重、交集、并集 | 课程性质多选筛选 |
| 栈 / 队列 | 先进后出 / 先进先出 | 路由导航栈 |
| 树 | 层级结构 | 专业-方向-班级层级 |
| 图 | 网状关系 | 知识图谱（未来扩展） |

### 5.3 算法

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 搜索算法 | 线性搜索、模糊匹配 | 课程名搜索、教师搜索 |
| 排序算法 | 按学分、序号排序 | 课程排序 |
| 防抖算法 | 延迟执行 | 搜索输入优化 |
| 分页算法 | offset/limit | 课程列表分页 |
| 拼音匹配 | 拼音首字母提取与匹配 | 教师拼音缩写搜索 |

### 5.4 数据库原理

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 关系模型 | 表、字段、主键、外键 | 数据库表设计 |
| 范式设计 | 1NF、2NF、3NF | 避免数据冗余 |
| 索引原理 | B+ 树 | 查询性能优化 |
| 事务 ACID | 原子性、一致性、隔离性、持久性 | 数据写入安全 |
| SQL 优化 | EXPLAIN、慢查询 | 接口性能调优 |

### 5.5 操作系统

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 进程与线程 | 并发执行 | Gunicorn 多进程模型 |
| 文件系统 | 权限、路径 | 静态资源管理 |
| 环境变量 | PATH、系统配置 | .env 配置管理 |
| Systemd | 服务管理 | 开机自启、进程守护 |

---

## 六、安全基础

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 密码哈希 | bcrypt / SHA256 | 用户密码存储 |
| JWT 安全 | 签名算法、过期时间 | 用户认证 |
| 数据脱敏 | 学号、姓名部分隐藏 | 学生信息展示 |
| SQL 注入防护 | 参数化查询 | ORM 自动防护 |
| XSS 防护 | 输入过滤、输出转义 | 用户反馈内容 |
| CORS 配置 | 允许的域名白名单 | 跨域安全 |
| HTTPS | TLS 加密传输 | 生产环境通信 |

---

## 七、软件工程

| 知识点 | 说明 | 在本项目中的应用 |
|--------|------|------------------|
| 前后端分离架构 | SPA + REST API | 整体架构 |
| MVC 模式 | Model-View-Controller | 后端分层设计 |
| 组件化开发 | 页面拆分为独立组件 | Vue 组件设计 |
| 版本控制 | Git 工作流 | 代码管理 |
| 环境管理 | 开发 / 测试 / 生产 | 多环境配置 |
| 日志管理 | 分级日志、日志轮转 | 错误追踪 |
| 错误处理 | 统一异常处理、友好提示 | 用户反馈 |
| 代码规范 | ESLint、PEP 8 | 代码质量 |

---

> **说明**：本文档覆盖了开发本课程推荐系统所需的核心基础知识。标注"未来扩展"的知识点尚未在当前版本中实现，可作为后续学习方向。
