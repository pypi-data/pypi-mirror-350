import os
from shared_architecture.config.config_loader import config_loader

def test_config_loader_reads_existing_key(monkeypatch):
    monkeypatch.setenv("TEST_CONFIG_KEY", "test_value")
    value = config_loader.get("TEST_CONFIG_KEY")
    assert value == "test_value"

def test_config_loader_returns_default_when_missing():
    value = config_loader.get("NON_EXISTENT_KEY", default="default_value")
    assert value == "default_value"
