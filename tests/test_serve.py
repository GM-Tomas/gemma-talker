from gemma_talker.serve import HOST, PORT, _opencode_snippet


def test_opencode_snippet_contains_required_fields():
    filename = "google_gemma-4-E2B-it-Q4_K_M.gguf"
    snippet = _opencode_snippet(filename)

    assert f"http://{HOST}:{PORT}/v1" in snippet
    assert filename in snippet
    assert "@ai-sdk/openai-compatible" in snippet
    assert "gemma-local" in snippet


def test_opencode_snippet_reflects_custom_filename():
    snippet = _opencode_snippet("custom-model-Q8_0.gguf")

    assert "custom-model-Q8_0.gguf" in snippet
    assert "google_gemma-4-E2B" not in snippet
