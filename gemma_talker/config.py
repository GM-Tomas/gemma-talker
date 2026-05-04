from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class ChatConfig:
    repo_id: str
    filename: str
    history_file: Path
    n_gpu_layers: int
    n_ctx: int
    temperature: float
    max_tokens: int

    @classmethod
    def from_env(cls) -> "ChatConfig":
        return cls(
            repo_id=os.getenv("GEMMA_TALKER_REPO_ID", "bartowski/google_gemma-4-E2B-it-GGUF"),
            filename=os.getenv("GEMMA_TALKER_MODEL_FILE", "google_gemma-4-E2B-it-Q4_K_M.gguf"),
            history_file=Path(
                os.getenv("GEMMA_TALKER_HISTORY", str(Path.home() / ".gemma_chat_history"))
            ),
            n_gpu_layers=int(os.getenv("GEMMA_TALKER_GPU_LAYERS", "-1")),
            n_ctx=int(os.getenv("GEMMA_TALKER_CTX", "4096")),
            temperature=float(os.getenv("GEMMA_TALKER_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("GEMMA_TALKER_MAX_TOKENS", "2048")),
        )
