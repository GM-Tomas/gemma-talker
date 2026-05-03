import os
import tempfile
from pathlib import Path
import pytest
from unittest.mock import MagicMock

# Asegurarse de que no falle la importación aunque no esté instalado llama_cpp aún
import sys
sys.modules['llama_cpp'] = MagicMock()

import chat_gemma
from chat_gemma import save_conversation, stream_response

def test_save_conversation():
    history = [
        {"role": "user", "content": "Hola Gemma"},
        {"role": "assistant", "content": "¡Hola! ¿Cómo puedo ayudarte hoy?"}
    ]
    system_prompt = "Sos un asistente útil."
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp:
        tmp_name = tmp.name

    try:
        saved_file = save_conversation(history, system_prompt, fname=tmp_name)
        assert saved_file == tmp_name
        
        content = Path(tmp_name).read_text(encoding="utf-8")
        
        assert f"# Chat con {chat_gemma.FILENAME}" in content
        assert "> **System:** Sos un asistente útil." in content
        assert "**Vos**\n\nHola Gemma" in content
        assert "**Gemma**\n\n¡Hola! ¿Cómo puedo ayudarte hoy?" in content
    finally:
        os.unlink(tmp_name)

def test_stream_response_success():
    messages = [{"role": "user", "content": "Hola"}]
    
    # Mockear el modelo Llama global
    chat_gemma.llm = MagicMock()
    
    # Simular el stream de llama-cpp-python
    def mock_stream():
        yield {"choices": [{"delta": {"content": "Hola "}}]}
        yield {"choices": [{"delta": {"content": "mundo!"}}]}
        
    chat_gemma.llm.create_chat_completion.return_value = mock_stream()
    
    response_text = stream_response(messages)
    assert response_text == "Hola mundo!"

def test_stream_response_error():
    messages = [{"role": "user", "content": "Hola"}]
    
    # Simular que el modelo no está instanciado o tira error
    chat_gemma.llm = MagicMock()
    chat_gemma.llm.create_chat_completion.side_effect = Exception("Llama no inicializado")
    
    response_text = stream_response(messages)
    assert response_text is None
