import sys

from gemma_talker.config import ChatConfig

HOST = "127.0.0.1"
PORT = 8000


def _opencode_snippet(filename: str) -> str:
    return f"""
Pega esto en tu opencode.json (o en ~/.config/opencode/config.json):

{{
  "$schema": "https://opencode.ai/config.json",
  "provider": {{
    "gemma-local": {{
      "npm": "@ai-sdk/openai-compatible",
      "name": "Gemma Local",
      "options": {{
        "baseURL": "http://{HOST}:{PORT}/v1"
      }},
      "models": {{
        "{filename}": {{
          "name": "Gemma 4 E2B",
          "limit": {{
            "context": 32768,
            "output": 2048
          }}
        }}
      }}
    }}
  }}
}}
"""


def serve() -> int:
    config = ChatConfig.from_env()

    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("Error: falta instalar huggingface-hub.", file=sys.stderr)
        return 1

    try:
        from llama_cpp.server.app import create_app
        from llama_cpp.server.settings import ModelSettings, ServerSettings
    except ImportError:
        print(
            "Error: el servidor requiere dependencias extra.\n"
            "Instalalas con: pip install 'llama-cpp-python[server]'",
            file=sys.stderr,
        )
        return 1

    try:
        import uvicorn
    except ImportError:
        print("Error: falta instalar uvicorn.", file=sys.stderr)
        return 1

    print(f"Ubicando modelo {config.filename}...")
    model_path = hf_hub_download(repo_id=config.repo_id, filename=config.filename)

    print(f"\nServidor OpenAI-compatible iniciando en http://{HOST}:{PORT}/v1")
    print(_opencode_snippet(config.filename))

    model_settings = [
        ModelSettings(
            model=str(model_path),
            n_gpu_layers=config.n_gpu_layers,
            n_ctx=config.n_ctx,
            model_alias=config.filename,
            logits_all=False,
        )
    ]
    app = create_app(server_settings=ServerSettings(), model_settings=model_settings)
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
    return 0
