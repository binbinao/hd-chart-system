"""Tests for hd_api.database reliability: SQLite WAL, busy_timeout, indexes,
and a package-anchored default DB path. Uses pytest tmp_path for isolation so
the real hd_records.db is never touched.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine

from hd_api.database import Base, ChartRecord


def _fresh_engine(tmp_path):
    """Build a DB the same way production does, against a temp file."""
    from hd_api.database import create_db_engine
    engine = create_db_engine(str(tmp_path / "test.db"))
    Base.metadata.create_all(engine)
    return engine


class TestSQLiteWAL:
    """Concurrent writers must not hit 'database is locked'. WAL + busy_timeout
    + a connection timeout lets writers wait instead of failing on first lock.
    """

    def test_journal_mode_is_wal(self, tmp_path):
        engine = _fresh_engine(tmp_path)
        with engine.connect() as conn:
            mode = conn.exec_driver_sql("PRAGMA journal_mode").scalar()
            assert str(mode).lower() == "wal"

    def test_busy_timeout_is_set(self, tmp_path):
        engine = _fresh_engine(tmp_path)
        with engine.connect() as conn:
            bt = conn.exec_driver_sql("PRAGMA busy_timeout").scalar()
            assert int(bt) >= 5000


class TestIndexes:
    """/records filters on type_key/profile and sorts by created_at DESC; without
    indexes those are full scans plus a count scan.
    """

    def test_filter_indexes_exist(self, tmp_path):
        from hd_api.database import init_db
        engine = _fresh_engine(tmp_path)
        init_db(engine)  # idempotent index creation
        with engine.connect() as conn:
            rows = conn.exec_driver_sql(
                "SELECT name FROM sqlite_master WHERE type='index' "
                "AND tbl_name='chart_records'"
            ).fetchall()
            names = {r[0] for r in rows}
            assert "ix_chart_records_type_key" in names
            assert "ix_chart_records_profile" in names
            assert "ix_chart_records_created_at" in names


class TestDefaultDbPath:
    """Default DB path must be package-anchored (absolute), not cwd-relative, so
    launching from another directory does not silently open an empty DB.
    """

    def test_default_is_absolute_and_named(self, monkeypatch):
        monkeypatch.delenv("HD_DB_PATH", raising=False)
        from hd_api.database import resolve_db_path
        path = resolve_db_path()
        assert os.path.isabs(path)
        assert os.path.basename(path) == "hd_records.db"

    def test_env_override_passthrough(self, monkeypatch):
        monkeypatch.setenv("HD_DB_PATH", "custom.db")
        from hd_api.database import resolve_db_path
        assert resolve_db_path() == "custom.db"
