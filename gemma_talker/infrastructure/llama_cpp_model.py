from typing import Iterable, Sequence

from gemma_talker.config import ChatConfig
from gemma_talker.domain.messages import ChatMessage


class LlamaCppChatModel:
    def __init__(self, llama: object, temperature: float, max_tokens: int) -> None:
        self._llama = llama
        self._temperature = temperature
        self._max_tokens = max_tokens

    @classmethod
    def from_huggingface(cls, config: ChatConfig) -> "LlamaCppChatModel":
        try:
            from huggingface_hub import hf_hub_download
        except ImportError as exc:
            raise RuntimeError("Falta instalar huggingface-hub.") from exc

        try:
            from llama_cpp import Llama
        except ImportError as exc:
            raise RuntimeError("Falta instalar llama-cpp-python.") from exc

        model_path = hf_hub_download(repo_id=config.repo_id, filename=config.filename)
        llama = Llama(
            model_path=model_path,
            n_gpu_layers=config.n_gpu_layers,
            n_ctx=config.n_ctx,
            verbose=False,
        )
        return cls(llama, temperature=config.temperature, max_tokens=config.max_tokens)

    def stream_chat(self, messages: Sequence[ChatMessage]) -> Iterable[str]:
        stream = self._llama.create_chat_completion(
            messages=[message.to_dict() for message in messages],
            stream=True,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
        )

        for chunk in stream:
            choices = chunk.get("choices", [])
            if not choices:
                continue

            delta = choices[0].get("delta", {})
            content = delta.get("content")
            if content:
                yield content
