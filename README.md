# 🔮 Human Design Chart System

人类图（Human Design）全栈计算系统——从天文星历到 SVG 图表到中文解读。

## 功能

- **🧮 计算引擎** (`hd_calc/`) — 基于 pyswisseph Moshier 星历的精确天文计算，Newton-Raphson 迭代求解 Design 日期，自动推导类型/权威/通道/中心/人生角色
- **🎨 SVG 渲染** (`hd_render/`) — 传统 Human Design Bodygraph 图表生成，暗色主题，响应式 SVG
- **📖 解读引擎** (`hd_interp/`) — 64 闸门 + 36 通道 + 9 中心 + 12 人生角色的完整中文解读，支持 Markdown/JSON/纯文本输出
- **🌐 REST API** (`hd_api/`) — FastAPI 服务，含交互式 Web UI 和 Swagger 文档

## 快速开始

```bash
# 安装依赖
pip install pyswisseph fastapi uvicorn pydantic

# 计算一张人类图
python -c "
from hd_calc import calculate_chart, CalculateRequest
req = CalculateRequest(year=1990, month=6, day=15, hour=10, minute=30, timezone_offset=8, lat=39.9, lng=116.4)
chart = calculate_chart(req)
print(f'{chart.type_zh} {chart.profile} {chart.authority_zh}')
"

# 生成 SVG Bodygraph
python -c "
from hd_calc import calculate_chart, CalculateRequest
from hd_render import render_bodygraph
from adapters import chart_to_render_dict
req = CalculateRequest(year=1990, month=6, day=15, hour=10, minute=30, timezone_offset=8, lat=39.9, lng=116.4)
chart = calculate_chart(req)
svg = render_bodygraph(chart_to_render_dict(chart), output_path='bodygraph.svg')
"

# 获取中文解读
python -c "
from hd_calc import calculate_chart, CalculateRequest
from hd_interp import generate_reading
from hd_interp.formatter import format_reading_markdown
req = CalculateRequest(year=1990, month=6, day=15, hour=10, minute=30, timezone_offset=8, lat=39.9, lng=116.4)
chart = calculate_chart(req)
reading = generate_reading(chart)
print(format_reading_markdown(reading))
"

# 启动 API 服务
python -m hd_api.main
# 访问 http://localhost:18090 体验 Web UI
# API 文档 http://localhost:18090/docs
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/chart` | 计算人类图数据 |
| POST | `/bodygraph` | 生成 SVG Bodygraph |
| POST | `/reading` | 计算 + 生成中文解读 |
| GET | `/gate/{n}` | 闸门信息 (1-64) |
| GET | `/channel/{g1}/{g2}` | 通道信息 |
| GET | `/type/{name}` | 类型信息 |

### 请求参数

```json
{
  "year": 1982,
  "month": 10,
  "day": 9,
  "hour": 21,
  "minute": 45,
  "timezone_offset": 8,
  "lat": 30.94,
  "lng": 118.75
}
```

## 项目结构

```
hd-chart-system/
├── hd_constants.py       # 共享常量（64闸门/36通道/9中心/5类型）
├── adapters.py           # dataclass → dict 适配层
├── hd_calc/              # 计算引擎
│   ├── models.py         # 数据类定义
│   ├── calculator.py     # pyswisseph + Newton-Raphson
│   └── analysis.py       # 通道/中心/类型/权威推导
├── hd_render/            # SVG 渲染
│   ├── styles.py         # 配色/布局常量
│   └── renderer.py       # Bodygraph 生成
├── hd_interp/            # 解读引擎
│   ├── interpret.py      # 生成中文解读
│   ├── formatter.py      # Markdown/JSON/纯文本输出
│   └── readings/         # 64闸门+36通道+9中心+12角色解读文本
│       ├── gate_readings.py
│       ├── channel_readings.py
│       ├── center_readings.py
│       ├── type_readings.py
│       └── profile_readings.py
├── hd_api/               # FastAPI 服务
│   ├── app.py            # REST API 端点
│   ├── dependencies.py   # 依赖注入
│   ├── main.py           # uvicorn 入口
│   └── static/           # Web UI 前端
└── tests/                # 测试
```

## 技术说明

### 星历精度
- 使用 pyswisseph 的 Moshier 内置星历，无需下载外部星历文件
- Moshier 精度约 ±0.5-1°，在闸门边界处可能与专业软件（bodygraph.com、myBodyGraph 等）产生差异
- 如需更高精度，可下载 Swiss Ephemeris .se1 文件并修改 `calculator.py` 中的 flag

### Design 日期计算
- Design 日期定义为：太阳位置 = Personality 太阳 - 88°
- 使用 Newton-Raphson 迭代法求解，需启用 `FLG_SPEED` 标志获取行星速度
- ⚠️ 不加 `FLG_SPEED` 会导致速度为 0，迭代不收敛，Design 侧所有行星位置偏移

### 支持的 Human Design 要素
- 5 种类型：显示者、生产者、显示生产者、投射者、反映者
- 7 种权威：荐骨型、情绪型、自我型、意志力型、直觉型、环境型、月周期型
- 36 条通道（含中英文名称）
- 64 个闸门（含中英文名称、易经对应）
- 9 个能量中心
- 12 个人生角色
- 192 种人生交叉

## License

MIT

---

_Built with pyswisseph + FastAPI. Powered by Moshier Ephemeris._
