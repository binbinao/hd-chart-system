"""Tests for hd_api.ai_service configuration exposure.

get_ai_config is unauthenticated and must not leak internal topology
(base_url of a self-hosted provider), and must not report a whitespace-only
key as configured.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestGetAiConfig:
    def test_does_not_expose_base_url(self, monkeypatch):
        monkeypatch.setenv("AI_API_KEY", "sk-test")
        monkeypatch.setenv("AI_BASE_URL", "http://internal-host:8080/v1")
        monkeypatch.setenv("AI_MODEL", "gpt-4o")
        from hd_api.ai_service import get_ai_config
        cfg = get_ai_config()
        assert "base_url" not in cfg
        assert cfg["configured"] is True
        assert cfg.get("model") == "gpt-4o"

    def test_whitespace_only_key_is_not_configured(self, monkeypatch):
        monkeypatch.setenv("AI_API_KEY", "   ")
        from hd_api.ai_service import get_ai_config
        assert get_ai_config()["configured"] is False
