"""Database module for persisting chart calculation records."""
import json
import os
from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, Integer, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Database file lives next to the running script (project root when run via `python -m hd_api.main`)
_DB_PATH = os.environ.get("HD_DB_PATH", "hd_records.db")
_DATABASE_URL = f"sqlite:///{_DB_PATH}"

engine = create_engine(_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class ChartRecord(Base):
    """Persisted record of a single chart calculation."""

    __tablename__ = "chart_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Birth data (request params)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)
    timezone_offset = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    # Key results (indexed for filtering)
    type_key = Column(Text)
    type_zh = Column(Text)
    authority_zh = Column(Text)
    profile = Column(Text)
    definition_type = Column(Text)
    channels_json = Column(Text)  # JSON array of channel pairs
    incarnation_cross_zh = Column(Text)

    # Full result blob for complete reconstruction
    result_json = Column(Text)


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a database session (for use with FastAPI Depends)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_record(db: Session, request_data: dict, chart_dict: dict) -> ChartRecord:
    """Save a chart calculation record to the database.

    Args:
        db: SQLAlchemy session
        request_data: dict with birth data (year, month, day, hour, minute, timezone_offset, lat, lng)
        chart_dict: the full chart result dict as returned by _chart_to_dict()

    Returns:
        The created ChartRecord instance.
    """
    channels = chart_dict.get("channels", [])
    channels_summary = json.dumps(
        [[ch["gate1"], ch["gate2"]] for ch in channels], ensure_ascii=False
    )

    record = ChartRecord(
        year=request_data["year"],
        month=request_data["month"],
        day=request_data["day"],
        hour=request_data["hour"],
        minute=request_data["minute"],
        timezone_offset=request_data["timezone_offset"],
        lat=request_data["lat"],
        lng=request_data["lng"],
        type_key=chart_dict.get("type_key"),
        type_zh=chart_dict.get("type_zh"),
        authority_zh=chart_dict.get("authority_zh"),
        profile=chart_dict.get("profile"),
        definition_type=chart_dict.get("definition_type"),
        channels_json=channels_summary,
        incarnation_cross_zh=chart_dict.get("incarnation_cross_zh"),
        result_json=json.dumps(chart_dict, ensure_ascii=False),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
