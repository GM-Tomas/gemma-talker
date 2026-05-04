import os

from gemma_talker.config import ChatConfig


def test_default_model_is_gemma4_e2b():
    config = ChatConfig.from_env()

    assert config.repo_id == "bartowski/google_gemma-4-E2B-it-GGUF"
    assert config.filename == "google_gemma-4-E2B-it-Q4_K_M.gguf"


def test_model_overridable_via_env(monkeypatch):
    monkeypatch.setenv("GEMMA_TALKER_REPO_ID", "bartowski/gemma-2-2b-it-GGUF")
    monkeypatch.setenv("GEMMA_TALKER_MODEL_FILE", "gemma-2-2b-it-Q4_K_M.gguf")

    config = ChatConfig.from_env()

    assert config.repo_id == "bartowski/gemma-2-2b-it-GGUF"
    assert config.filename == "gemma-2-2b-it-Q4_K_M.gguf"
