# 📍 广州 POI 地理信息系统

基于 **FastAPI + PostGIS + OpenLayers** 的广州兴趣点（POI）查询与可视化系统，支持 POI 增删改查、分类筛选、关键词搜索、附近查询、矩形框查询、统计导出等 16 个接口，前端通过 OpenLayers 地图展示 POI 分布，支持交互式操作。

## ✨ 功能特性

- ✅ POI 增删改查（CRUD）
- ✅ 按类别筛选 POI
- ✅ 关键词模糊搜索（名称 + 描述）
- ✅ 附近搜索（指定坐标 + 半径）
- ✅ 矩形框搜索（BBox）
- ✅ GeoJSON 格式导出
- ✅ 统计数据（总数、分类统计、平均评分）
- ✅ 用户评价系统
- ✅ OpenLayers 交互式地图
- ✅ 响应式布局（PC + 移动端）

## 🛠 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI + Python 3.11 |
| 数据库 | PostgreSQL 15 + PostGIS 3.3 |
| ORM | SQLAlchemy 2.0 + Pydantic v2 |
| 前端地图 | OpenLayers 7.x (CDN) |
| 前端样式 | 原生 CSS + Flexbox |
| 容器化 | Docker + Docker Compose |

## 🚀 快速启动

### Docker 一键启动

```bash
docker-compose up -d
```

启动后：
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs
- 前端页面：打开 `frontend/index.html`

### 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
python -m app.utils.seed_data
uvicorn app.main:app --reload --port 8000

# 前端：直接用浏览器打开 frontend/index.html
```

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/pois` | GET | 列表查询 |
| `/api/pois/{id}` | GET | 单个 POI |
| `/api/pois` | POST | 创建 POI |
| `/api/pois/{id}` | PUT | 更新 POI |
| `/api/pois/{id}` | DELETE | 删除 POI |
| `/api/pois/filter/category/{id}` | GET | 按分类筛选 |
| `/api/pois/search/?keyword=` | GET | 关键词搜索 |
| `/api/pois/nearby/` | GET | 附近搜索 |
| `/api/pois/bbox/` | GET | 矩形框搜索 |
| `/api/pois/geojson/all` | GET | GeoJSON 全量 |
| `/api/pois/geojson/{id}` | GET | 单个 GeoJSON |
| `/api/pois/stats/` | GET | 统计数据 |
| `/api/pois/{id}/reviews` | GET | POI 评价 |
| `/api/pois/reviews` | POST | 添加评价 |
| `/api/categories` | GET/POST | 类别管理 |

> 完整文档：http://localhost:8000/docs

## 📁 目录结构

```
guangzhou-poi-gis/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI 入口
│   │   ├── config.py         # 配置管理
│   │   ├── database.py       # 数据库连接
│   │   ├── models/           # 数据模型
│   │   ├── schemas/          # Pydantic Schema
│   │   ├── routers/          # 路由（16 个接口）
│   │   ├── services/         # 地理计算服务
│   │   └── utils/            # 种子数据
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html            # 主页面
│   ├── css/style.css         # 样式
│   └── js/                   # 前端逻辑
├── docker-compose.yml
├── .env.example
└── README.md
```

## 📄 License

MIT

## GitHub 仓库推送

1. 在 GitHub 创建新仓库（不要初始化 README）：https://github.com/new
2. 设置远程地址并推送：

```bash
git remote add origin https://github.com/YOUR_USERNAME/guangzhou-poi-gis.git
git branch -M main
git push -u origin main
```
