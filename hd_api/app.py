"""FastAPI application for Human Design chart and reading API."""
import hashlib
import json
from collections import OrderedDict
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import os

from hd_api.dependencies import (
    do_calculate, do_reading, get_gate_info, get_channel_info, get_type_info,
)
from hd_api.database import init_db, get_db, save_record, ChartRecord
from hd_api.ai_service import get_ai_config, stream_ai_reading
from hd_interp.readings.gate_readings import GATE_READINGS
from hd_interp.readings.channel_readings import CHANNEL_READINGS

app = FastAPI(
    title="Human Design Chart API",
    description="Calculate Human Design charts and generate Chinese interpretations",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


# Simple LRU cache with max size to prevent unbounded memory growth
_CACHE_MAX_SIZE = 256
_reading_cache: OrderedDict = OrderedDict()


def _cache_put(key: str, value: dict):
    """Add to cache, evicting oldest entry if at capacity."""
    _reading_cache[key] = value
    _reading_cache.move_to_end(key)
    while len(_reading_cache) > _CACHE_MAX_SIZE:
        _reading_cache.popitem(last=False)


class ChartRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100, description="Birth year")
    month: int = Field(..., ge=1, le=12, description="Birth month")
    day: int = Field(..., ge=1, le=31, description="Birth day")
    hour: int = Field(..., ge=0, le=23, description="Birth hour (0-23)")
    minute: int = Field(..., ge=0, le=59, description="Birth minute")
    timezone_offset: float = Field(8.0, description="Timezone offset from UTC (e.g. +8 for CST)")
    lat: float = Field(..., ge=-90, le=90, description="Birth latitude")
    lng: float = Field(..., ge=-180, le=180, description="Birth longitude")


def _chart_id(req: ChartRequest) -> str:
    """Generate a stable cache key from request params."""
    raw = f"{req.year}-{req.month}-{req.day}-{req.hour}-{req.minute}-{req.timezone_offset}-{req.lat}-{req.lng}"
    return hashlib.md5(raw.encode()).hexdigest()


def _chart_to_dict(chart) -> dict:
    """Convert ChartResult to a JSON-serializable dict."""
    def _activation_to_dict(a):
        return {'longitude': a.longitude, 'gate': a.gate, 'line': a.line}

    def _center_to_dict(c):
        return {
            'name': c.name, 'name_zh': c.name_zh, 'name_en': c.name_en,
            'is_defined': c.is_defined, 'activated_gates': c.activated_gates,
        }

    def _channel_to_dict(ch):
        return {
            'gate1': ch.gate1, 'gate2': ch.gate2,
            'name_zh': ch.name_zh, 'name_en': ch.name_en,
            'personality_gates': ch.personality_gates,
            'design_gates': ch.design_gates,
        }

    return {
        'type_key': chart.type_key,
        'type_zh': chart.type_zh,
        'type_en': chart.type_en,
        'authority_zh': chart.authority_zh,
        'authority_en': chart.authority_en,
        'profile': chart.profile,
        'profile_conscious_line': chart.profile_conscious_line,
        'profile_design_line': chart.profile_design_line,
        'definition_type': chart.definition_type,
        'incarnation_cross_zh': chart.incarnation_cross_zh,
        'incarnation_cross_en': chart.incarnation_cross_en,
        'incarnation_cross_gates': chart.incarnation_cross_gates,
        'design_date_approx': chart.design_date_approx,
        'channels': [_channel_to_dict(ch) for ch in chart.channels],
        'centers': {k: _center_to_dict(v) for k, v in chart.centers.items()},
        'personality': {k: _activation_to_dict(v) for k, v in chart.personality.items()},
        'design': {k: _activation_to_dict(v) for k, v in chart.design.items()},
    }


@app.post("/chart")
def calculate_chart_api(req: ChartRequest, db: Session = Depends(get_db)):
    """Calculate a Human Design chart from birth data."""
    try:
        chart = do_calculate(
            req.year, req.month, req.day, req.hour, req.minute,
            req.timezone_offset, req.lat, req.lng,
        )
        chart_dict = _chart_to_dict(chart)
        # Persist to database
        save_record(db, req.model_dump(), chart_dict)
        return chart_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reading")
def calculate_reading_api(req: ChartRequest, output_format: Optional[str] = "json", db: Session = Depends(get_db)):
    """Calculate chart and generate full Chinese interpretation."""
    try:
        chart = do_calculate(
            req.year, req.month, req.day, req.hour, req.minute,
            req.timezone_offset, req.lat, req.lng,
        )
        reading = do_reading(chart)
        chart_dict = _chart_to_dict(chart)

        # Persist to database
        save_record(db, req.model_dump(), chart_dict)

        cid = _chart_id(req)
        _cache_put(cid, {'chart': chart_dict, 'reading': reading})

        result = {'chart_id': cid, 'chart': chart_dict, 'reading': reading}

        if output_format == "markdown":
            from hd_interp.formatter import format_reading_markdown
            result['reading_markdown'] = format_reading_markdown(reading)
        elif output_format == "plain":
            from hd_interp.formatter import format_reading_plain
            result['reading_plain'] = format_reading_plain(reading)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reading/{chart_id}")
def get_cached_reading(chart_id: str):
    """Retrieve a cached reading by chart_id."""
    if chart_id not in _reading_cache:
        raise HTTPException(status_code=404, detail="Reading not found")
    return _reading_cache[chart_id]


@app.get("/gate/{gate_number}")
def gate_info(gate_number: int):
    """Get detailed info for a specific gate (1-64)."""
    if gate_number < 1 or gate_number > 64:
        raise HTTPException(status_code=400, detail="Gate number must be 1-64")
    info = get_gate_info(gate_number)
    if not info:
        raise HTTPException(status_code=404, detail="Gate not found")
    # Add reading
    reading = GATE_READINGS.get(gate_number, {})
    return {**info, 'theme': reading.get('theme', ''), 'conscious': reading.get('conscious', ''), 'unconscious': reading.get('unconscious', '')}


@app.get("/channel/{g1}/{g2}")
def channel_info(g1: int, g2: int):
    """Get info for a specific channel by its two gate numbers."""
    info = get_channel_info(g1, g2)
    if not info:
        raise HTTPException(status_code=404, detail="Channel not found")
    # Add reading
    ch_key = (g1, g2) if (g1, g2) in CHANNEL_READINGS else (g2, g1)
    reading = CHANNEL_READINGS.get(ch_key, {})
    return {**info, 'body': reading.get('body', '')}


class BodygraphRequest(ChartRequest):
    """Alias for ChartRequest used by the bodygraph endpoint."""
    pass


@app.post("/bodygraph")
def render_bodygraph_api(req: BodygraphRequest):
    """Calculate chart and return SVG bodygraph."""
    try:
        chart = do_calculate(
            req.year, req.month, req.day, req.hour, req.minute,
            req.timezone_offset, req.lat, req.lng,
        )
        from adapters import chart_to_render_dict
        from hd_render import render_bodygraph as _render
        render_data = chart_to_render_dict(chart)
        svg = _render(render_data)
        return Response(content=svg, media_type="image/svg+xml")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/type/{type_name}")
def type_info(type_name: str):
    """Get info for a specific type."""
    from hd_constants import TYPES
    info = get_type_info(type_name)
    if not info:
        raise HTTPException(status_code=404, detail=f"Type '{type_name}' not found. Valid types: {list(TYPES.keys())}")
    from hd_interp.readings.type_readings import TYPE_READINGS
    type_reading = TYPE_READINGS.get(type_name, {})
    return {**info, 'title': type_reading.get('title', ''), 'body': type_reading.get('body', '')}


# ============================================================
# Records (history) endpoints
# ============================================================

@app.get("/records")
def list_records(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    type_key: Optional[str] = Query(None, description="Filter by type key (e.g. Generator)"),
    profile: Optional[str] = Query(None, description="Filter by profile (e.g. 1/5)"),
    db: Session = Depends(get_db),
):
    """List chart calculation history with pagination and optional filters."""
    query = db.query(ChartRecord)
    if type_key:
        query = query.filter(ChartRecord.type_key == type_key)
    if profile:
        query = query.filter(ChartRecord.profile == profile)

    total = query.count()
    records = (
        query.order_by(ChartRecord.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    items = []
    for r in records:
        items.append({
            "id": r.id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "year": r.year,
            "month": r.month,
            "day": r.day,
            "hour": r.hour,
            "minute": r.minute,
            "timezone_offset": r.timezone_offset,
            "lat": r.lat,
            "lng": r.lng,
            "type_key": r.type_key,
            "type_zh": r.type_zh,
            "authority_zh": r.authority_zh,
            "profile": r.profile,
            "definition_type": r.definition_type,
            "channels_json": r.channels_json,
            "incarnation_cross_zh": r.incarnation_cross_zh,
        })

    return {"total": total, "page": page, "size": size, "items": items}


@app.get("/records/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db)):
    """Get a single chart record by ID, including full result JSON."""
    record = db.query(ChartRecord).filter(ChartRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    result = {
        "id": record.id,
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "year": record.year,
        "month": record.month,
        "day": record.day,
        "hour": record.hour,
        "minute": record.minute,
        "timezone_offset": record.timezone_offset,
        "lat": record.lat,
        "lng": record.lng,
        "type_key": record.type_key,
        "type_zh": record.type_zh,
        "authority_zh": record.authority_zh,
        "profile": record.profile,
        "definition_type": record.definition_type,
        "channels_json": record.channels_json,
        "incarnation_cross_zh": record.incarnation_cross_zh,
        "result": json.loads(record.result_json) if record.result_json else None,
    }
    return result


# ============================================================
# AI Analysis endpoints
# ============================================================

@app.get("/ai-config")
def ai_config_status():
    """Check AI service configuration status."""
    return get_ai_config()


@app.post("/ai-reading")
def ai_reading(req: ChartRequest, db: Session = Depends(get_db)):
    """Generate AI-powered deep analysis of a Human Design chart (SSE stream)."""
    config = get_ai_config()
    if not config["configured"]:
        raise HTTPException(
            status_code=503,
            detail="AI 服务未配置。请设置 AI_API_KEY 环境变量。"
        )

    try:
        chart = do_calculate(
            req.year, req.month, req.day, req.hour, req.minute,
            req.timezone_offset, req.lat, req.lng,
        )
        # Persist to database
        chart_dict = _chart_to_dict(chart)
        save_record(db, req.model_dump(), chart_dict)

        return StreamingResponse(
            stream_ai_reading(chart),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount static files and serve index
_static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")

@app.get("/")
def index():
    _index = os.path.join(_static_dir, "index.html")
    if os.path.exists(_index):
        with open(_index, encoding='utf-8') as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Human Design API</h1><p>Use /docs for API reference</p>")
